import psutil
import time
from tqdm import tqdm
import sys

nic_name = "nic0"
sample_duration = 60
restart_nic = False
restart_threshold = 75
restart_thr_count = 3

is_tty = sys.stdout.isatty()
if not is_tty:
  print("!HEADLESS SERVICE! - no tty found")

drop_pct = lambda drops,total: (drops / total * 100) if total > 0 else 0
is_int = lambda n: True if isinstance(n, int) else n.is_integer() if isinstance(n, float) else False
def tqdm_sleep(seconds:int|float, desc:str|None=None, colour:str|None=None):
  if is_int(seconds):
    for sec in tqdm(range(int(seconds)), unit="s", desc=desc, colour=colour, leave=False, disable=not is_tty):
      time.sleep(1)
    return True

  for i in range(1,3+1):
    if is_int(seconds*(10**i)):
      for sec in tqdm(range(int(seconds*(10**i))), unit=["ds","cs","ms"][i], desc=desc, colour=colour, leave=False, disable=not is_tty):
        time.sleep(0.1**i)
      return True

  time.sleep(seconds)
  return False
class color:
  yellow = "\x1B[38;5;3m"
  rx_red = "\x1B[38;5;1m"
  tx_blue = "\x1B[38;5;4m"
  drop_red = "\x1B[38;5;1m"
  tt_green = "\x1B[38;5;2m"
  reset = "\x1B[0m"

  colors = [yellow,rx_red,tx_blue,tt_green,drop_red,reset]
  def rmstrs(msg:str):
    colors = color.colors
    rmsg = msg
    for clr in colors:
      rmsg = rmsg.replace(clr, "")
    return rmsg

last_rx = last_tx = last_rx_drops = last_tx_drops = None
fail_count = 0
while True:
  stats = psutil.net_io_counters(pernic=True)
  if nic_name in stats:
    data = stats[nic_name]
    total_rx, total_tx = data.packets_recv, data.packets_sent
    rx_drops, tx_drops = data.dropin, data.dropout

    if last_rx is not None and last_tx is not None and last_rx_drops is not None and last_tx_drops is not None:
      rx_pct = drop_pct(rx_drops-last_rx_drops, total_rx-last_rx)
      tx_pct = drop_pct(tx_drops-last_tx_drops, total_tx-last_tx)
      total_pct = drop_pct((rx_drops+tx_drops)-(last_rx_drops+last_tx_drops), (total_rx+total_tx)-(last_rx+last_tx))

      print_msg = f"{color.yellow}last {sample_duration}s:{color.reset}"
      print_msg += f"\n{color.rx_red}  Received: {total_rx-last_rx} {color.drop_red}(dropped: {rx_drops-last_rx_drops} | {rx_pct}%){color.reset}"
      print_msg += f"\n{color.tx_blue}  Transmitted: {total_tx-last_tx} {color.drop_red}(dropped: {tx_drops-last_tx_drops} | {tx_pct}%){color.reset}"
      print_msg += f"\n{color.yellow}  " + "-"*(max(len(i) for i in color.rmstrs(print_msg).split("\n")[1:])-2) + f"{color.reset}"
      print_msg += f"\n{color.tt_green}  Total: {(total_rx+total_tx)-(last_rx+last_tx)} {color.drop_red}(dropped: {(rx_drops+tx_drops)-(last_rx_drops+last_tx_drops)} | {total_pct}%){color.reset}"
      print_msg += f"\n{color.yellow}" + "="*max(len(i) for i in color.rmstrs(print_msg).split("\n")) + f"{color.reset}"

      print(print_msg)
      fail_count = fail_count + 1 if total_pct > restart_threshold else 0
      if restart_nic and fail_count >= restart_thr_count:
        restart_finished = False
        while not restart_finished:
          try:
            subprocess.run(f"ip link set dev {nic_name} down".split(" "), check=True)
            tqdm_sleep(2.5, desc="nic restart!", colour="red")
            subprocess.run(f"ip link set dev {nic_name} up".split(" "), check=True)
          except subprocess.CalledProcessError as e:
            print(f"nic restart failed:\n{e}")
    last_rx, last_rx_drops = total_rx, rx_drops
    last_tx, last_tx_drops = total_tx, tx_drops
    tqdm_sleep(sample_duration, desc="waiting...", colour="green")
  else:
    tqdm_sleep(10, desc="nic not found!", colour="red")
