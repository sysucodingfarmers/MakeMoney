export default {
  data: {
    tasks: [
        {
          id: 0,             //用于辨别任务的id
          name: '比武招亲1',           //任务名称
          publisher: '阿彤',      //任务发起者
          type: '问卷调查',           //任务类型
          start_time: '2019-10-10 10:00',     //任务开始时间:xxxx-xx-xx xx:xx
          end_time: '2019-10-20 10:00',       //任务结束时间:xxxx-xx-xx xx:xx
          pay: 100,             //任务报酬
          detail: '比武招亲是一项非常重要的事情，对于当代大学生来说，相亲还不算太晚但是必须',         //任务详情
          receiver: [         //任务接收者
            // { 
            //   name: '',           //接收者名字
            //   id: 0,             //接受者id，用于识别
            //   isfinished: false,  //是否完成该任务
            //   ispaid: false       //是否给予报酬
            // }
            {
              name: '陈咏强',
              id: 1,
              isfinished: false,
              ispaid: false
            },
            {
              name: '戴馨乐',
              id: 2,
              isfinished: false,
              ispaid: false
            },
            {
              name: '陈梓峰',
              id: 3,
              isfinished: false,
              ispaid: false
            }
          ],
          receiver_limit: 4,  //接收者人数限制
          finish_rate: 0,     //完成程度
          extra_content:{     //额外内容：包括图片数据以及问卷数据
            query: [
              {
              id: 0,
              type: "单选题",           //单选题
              content: {
                question: "你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗",
                option: [
                  {ans: "对", isSelected: false},
                  {ans: "错", isSelected: false}
                ]
              }
            },
            {
              id: 1,
              type: "多选题",           //多选题
              content: {
                question: "谁打球像蔡徐坤",
                option: [
                  {ans: "戴馨乐", isSelected: false},
                  {ans: "陈咏强", isSelected: false},
                  {ans: "陈梓峰", isSelected: false}
                ]
              }
            },
            {
              id: 2,
              type: "问答题",           //问答题
              content: {
                question: "如何评价打球像蔡徐坤这句话",
                answer: ""
              },
              limit: "text"
            }
            ],        //问卷
            images:[]         //图片
          }    
        },
        {
          id: 1,             //用于辨别任务的id
          name: '比武招亲2',           //任务名称
          publisher: '阿彤',      //任务发起者
          type: '问卷调查',           //任务类型
          start_time: '2019-10-10 10:00',     //任务开始时间:xxxx-xx-xx xx:xx
          end_time: '2019-10-20 10:00',       //任务结束时间:xxxx-xx-xx xx:xx
          pay: 100,             //任务报酬
          detail: '比武招亲是一项非常重要的事情，对于当代大学生来说，相亲还不算太晚但是必须',         //任务详情
          receiver: [         //任务接收者
            // { 
            //   name: '',           //接收者名字
            //   id: 0,             //接受者id，用于识别
            //   isfinished: false,  //是否完成该任务
            //   ispaid: false       //是否给予报酬
            // }
            {
              name: '陈咏强',
              id: 1,
              isfinished: false,
              ispaid: false
            },
            {
              name: '戴馨乐',
              id: 2,
              isfinished: false,
              ispaid: false
            },
            {
              name: '陈梓峰',
              id: 3,
              isfinished: false,
              ispaid: false
            }
          ],
          receiver_limit: 4,  //接收者人数限制
          finish_rate: 0,     //完成程度
          extra_content:{     //额外内容：包括图片数据以及问卷数据
            query: [
              {
              id: 0,
              type: "单选题",           //单选题
              content: {
                question: "你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗",
                option: [
                  {ans: "对", isSelected: false},
                  {ans: "错", isSelected: false}
                ]
              }
            },
            {
              id: 1,
              type: "多选题",           //多选题
              content: {
                question: "谁打球像蔡徐坤",
                option: [
                  {ans: "戴馨乐", isSelected: false},
                  {ans: "陈咏强", isSelected: false},
                  {ans: "陈梓峰", isSelected: false}
                ]
              }
            },
            {
              id: 2,
              type: "问答题",           //问答题
              content: {
                question: "如何评价打球像蔡徐坤这句话",
                answer: ""
              },
              limit: "text"
            }
            ],        //问卷
            images:[]         //图片
          }    
        },
        {
          id: 2,             //用于辨别任务的id
          name: '比武招亲3',           //任务名称
          publisher: '阿彤',      //任务发起者
          type: '问卷调查',           //任务类型
          start_time: '2019-10-10 10:00',     //任务开始时间:xxxx-xx-xx xx:xx
          end_time: '2019-10-20 10:00',       //任务结束时间:xxxx-xx-xx xx:xx
          pay: 100,             //任务报酬
          detail: '比武招亲是一项非常重要的事情，对于当代大学生来说，相亲还不算太晚但是必须',         //任务详情
          receiver: [         //任务接收者
            // { 
            //   name: '',           //接收者名字
            //   id: 0,             //接受者id，用于识别
            //   isfinished: false,  //是否完成该任务
            //   ispaid: false       //是否给予报酬
            // }
            {
              name: '陈咏强',
              id: 1,
              isfinished: false,
              ispaid: false
            },
            {
              name: '戴馨乐',
              id: 2,
              isfinished: false,
              ispaid: false
            },
            {
              name: '陈梓峰',
              id: 3,
              isfinished: false,
              ispaid: false
            }
          ],
          receiver_limit: 4,  //接收者人数限制
          finish_rate: 0,     //完成程度
          extra_content:{     //额外内容：包括图片数据以及问卷数据
            query: [
              {
              id: 0,
              type: "单选题",           //单选题
              content: {
                question: "你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗",
                option: [
                  {ans: "对", isSelected: false},
                  {ans: "错", isSelected: false}
                ]
              }
            },
            {
              id: 1,
              type: "多选题",           //多选题
              content: {
                question: "谁打球像蔡徐坤",
                option: [
                  {ans: "戴馨乐", isSelected: false},
                  {ans: "陈咏强", isSelected: false},
                  {ans: "陈梓峰", isSelected: false}
                ]
              }
            },
            {
              id: 2,
              type: "问答题",           //问答题
              content: {
                question: "如何评价打球像蔡徐坤这句话",
                answer: ""
              },
              limit: "text"
            }
            ],        //问卷
            images:[]         //图片
          }    
        },
        {
          id: 3,             //用于辨别任务的id
          name: '比武招亲4',           //任务名称
          publisher: '阿彤',      //任务发起者
          type: '问卷调查',           //任务类型
          start_time: '2019-10-10 10:00',     //任务开始时间:xxxx-xx-xx xx:xx
          end_time: '2019-10-20 10:00',       //任务结束时间:xxxx-xx-xx xx:xx
          pay: 100,             //任务报酬
          detail: '比武招亲是一项非常重要的事情，对于当代大学生来说，相亲还不算太晚但是必须',         //任务详情
          receiver: [         //任务接收者
            // { 
            //   name: '',           //接收者名字
            //   id: 0,             //接受者id，用于识别
            //   isfinished: false,  //是否完成该任务
            //   ispaid: false       //是否给予报酬
            // }
            {
              name: '陈咏强',
              id: 1,
              isfinished: false,
              ispaid: false
            },
            {
              name: '戴馨乐',
              id: 2,
              isfinished: false,
              ispaid: false
            },
            {
              name: '陈梓峰',
              id: 3,
              isfinished: false,
              ispaid: false
            }
          ],
          receiver_limit: 4,  //接收者人数限制
          finish_rate: 0,     //完成程度
          extra_content:{     //额外内容：包括图片数据以及问卷数据
            query: [
              {
              id: 0,
              type: "单选题",           //单选题
              content: {
                question: "你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗你打球像蔡徐坤吗",
                option: [
                  {ans: "对", isSelected: false},
                  {ans: "错", isSelected: false}
                ]
              }
            },
            {
              id: 1,
              type: "多选题",           //多选题
              content: {
                question: "谁打球像蔡徐坤",
                option: [
                  {ans: "戴馨乐", isSelected: false},
                  {ans: "陈咏强", isSelected: false},
                  {ans: "陈梓峰", isSelected: false}
                ]
              }
            },
            {
              id: 2,
              type: "问答题",           //问答题
              content: {
                question: "如何评价打球像蔡徐坤这句话",
                answer: ""
              },
              limit: "text"
            }
            ],        //问卷
            images:[]         //图片
          }    
        }
      ]  
    
  }
}