function JsonToUrl(jsn, ip, type="task/") {
	var obj = JSON.parse(jsn);
	var url = [];
	for (var i in obj) {
		url.push(ip + type + obj[i]);
	}
	return url;
}
function GetAvatarUrl(filename, ip) {
  return ip + 'user/' + filename
}
module.exports = {
	JsonToUrl: JsonToUrl,
  GetAvatarUrl: GetAvatarUrl
}