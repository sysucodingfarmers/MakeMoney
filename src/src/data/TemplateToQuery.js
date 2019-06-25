//将后端传送的问卷数据转化


function change(data) {
	var questions = data.questions;
	var options = data.options;
	var types = data.types;
	var query = [];
	for (var i = 0; i < types.length; ++i) {
		if (types[i] == '数字题' || types[i] == '问答题') {
			var limit = types[i] == '数字题' ? 'number' : 'text';
			var temp = {
				id: i,
				type: '问答题',
				content: {
					question: questions[i],
					ans: ''
				},
				limit: limit
			}
			query.push(temp);
		}
		else if (types[i] == '多选题' || types[i] == '单选题') {
			var temp = {
				id: i,
				type: types[i],
				content: {
					question: questions[i],
					option: []
				}
			}
			options[i].forEach(item=>{
				temp.content.option.push({ ans: item, isSelected: false });
			})
			query.push(temp);
		}
	}

	return query;
}

module.exports = {
	change: change
}