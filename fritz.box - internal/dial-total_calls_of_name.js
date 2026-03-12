// INPUT VARIABLES
name_number = "" // (type: string) specifies Name/Number to search for
// INPUT VARIABLES

days = 0
hours = 0
minutes = 0
callCount = 0
for (let i of Array.from(document.getElementsByClassName("duration")).slice(1)) {
    if (i.parentElement.children[2].title == name_number || i.parentElement.children[2].innerText == name_number) {
        const timeStr = i.getAttribute('data-timestr')
        if (timeStr != '0:00') {
            const timeParts = timeStr.split(':')
            hours += Number(timeParts[0])
            minutes += Number(timeParts[1])
            console.log(`[${i.parentElement.children[0].getAttribute('datalabel')}]: ${timeStr}`)
            callCount += 1
        }
    }
}
hours += Math.floor(minutes / 60)
minutes -= (60 * Math.floor(minutes / 60))
days += Math.floor(hours / 24)
hours -= (24 * Math.floor(hours / 24))

finalOutputDuration = ""
if (days > 0) {
    finalOutputDuration += `${days.toString().padStart(2, '0')}d:`
}
if (hours > 0) {
    finalOutputDuration += `${hours.toString().padStart(2, '0')}h:`
}
finalOutputDuration += `${minutes.toString().padStart(2, '0')}m`
console.log(`Total: \n  - Calls: ${callCount}\n  - Duration: ${finalOutputDuration}`)