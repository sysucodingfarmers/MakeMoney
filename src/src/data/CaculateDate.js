function DateToString(val) {
	var date = new Date(val);
  	var month = date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth() + 1;
  	var currentDate = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
  	var hour = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
  	var minute = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
  	var datetime = date.getFullYear() + "-" + month + "-" + currentDate + " " + hour + ":" + minute;
  	return datetime;
}
//20XX-XX-XX XX:XX
function StringToDate(str) {
	str = str.replace(/\s/g, 'T');
	return new Date(str);
}
module.exports = {
	DateToString: DateToString,
	StringToDate: StringToDate
}