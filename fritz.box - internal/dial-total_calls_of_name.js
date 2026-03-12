// INPUT VARIABLES
name_number = "" // (type: string) specifies Name/Number to search for

// INPUT VARIABLES

d = 0
h = 0
m = 0
c = 0
for (let i of Array.from(document.getElementsByClassName("duration")).slice(1)) {
    if (i.parentElement.children[2].title==name_number) {
        if (i.getAttribute('data-timestr') != '0:00') {
            h += Number(i.getAttribute('data-timestr').split(':')[0])
            m += Number(i.getAttribute('data-timestr').split(':')[1])
            console.log(`[${i.parentElement.children[0].getAttribute('datalabel')}]: ${i.getAttribute('data-timestr')}`)
            c += 1
        }
    }
}
h += Math.floor(m / 60)
m -= (60 * Math.floor(m / 60))
d += Math.floor(h / 24)
h -= (24 * Math.floor(h / 24))
console.log(`Total: \n  - Calls: ${c}\n  - Duration: ${d}:${h}:${m}`)