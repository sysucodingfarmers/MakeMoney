import { VantComponent } from '../common/component';
import Toast from '../toast/toast'

const nextTick = () => new Promise(resolve => setTimeout(resolve, 20));
VantComponent({
    classes: ['title-class', 'content-class'],
    relation: {
        name: 'collapse-for-taskdetail',
        type: 'ancestor',
        linked(parent) {
            this.parent = parent;
        }
    },
    props: {
        name: null,
        title: null,
        value: null,
        icon: String,
        label: String,
        disabled: Boolean,
        clickable: Boolean,
        border: {
            type: Boolean,
            value: true
        },
        isLink: {
            type: Boolean,
            value: true
        },

        userid: {
            type: Number,
            value: 0
        },
        taskid: {
            type: Number,
            value: 0
        },
        tempid: {
            type: Number,
            value: 0
        },
        isfinished: {
            type: Boolean,
            value: false
        },
        ispaid: {
            type: Boolean,
            value: false
        },
        type: {
            type: String,
            value: ''
        },
        buttonleft: {
            type: String,
            value: '确认'
        },
        buttonright: {
            type: String,
            value: '打款'
        },
        reqeusturl: {
            type: String,
            value: 'http://makemoney.ink:5000/'
        }
    },
    data: {
        contentHeight: 0,
        expanded: false,
        transition: false
    },
    mounted() {
        this.updateExpanded()
            .then(nextTick)
            .then(() => {
            this.set({ transition: true });
        });
    },
    methods: {
        updateExpanded() {
            if (!this.parent) {
                return Promise.resolve();
            }
            const { value, accordion } = this.parent.data;
            const { children = [] } = this.parent;
            const { name } = this.data;
            const index = children.indexOf(this);
            const currentName = name == null ? index : name;
            const expanded = accordion
                ? value === currentName
                : (value || []).some((name) => name === currentName);
            const stack = [];
            if (expanded !== this.data.expanded) {
                stack.push(this.updateStyle(expanded));
            }
            stack.push(this.set({ index, expanded }));
            return Promise.all(stack);
        },
        updateStyle(expanded) {
            return this.getRect('.van-collapse-item__content')
                .then((rect) => rect.height)
                .then((height) => {
                if (expanded) {
                    return this.set({
                        contentHeight: height ? `${height}px` : 'auto'
                    });
                }
                else {
                    return this.set({ contentHeight: `${height}px` })
                        .then(nextTick)
                        .then(() => this.set({ contentHeight: 0 }));
                }
            });
        },
        onClick() {
            if (this.data.disabled) {
                return;
            }
            const { name, expanded } = this.data;
            const index = this.parent.children.indexOf(this);
            const currentName = name == null ? index : name;
            this.parent.switch(currentName, !expanded);
        },
        onTransitionEnd() {
            if (this.data.expanded) {
                this.set({
                    contentHeight: 'auto'
                });
            }
        },
        // 点击左边按钮
        LeftSubbmit() {
            var that = this
            if (this.data.buttonleft == '已确认') {
                wx.showToast({
                  title: '已经确认',
                  icon: 'success',
                  duration: 1000
                })
            }
            else if (this.data.buttonleft == '确认') {
                if (this.data.type == '问卷调查') {
                    wx.showToast({
                      title: '问卷还未完成',
                      icon: 'fail',
                      duration: 1000
                    })
                }
                else {
                    wx.request({
                        url: that.data.reqeusturl + 'task/finished',
                        method: 'POST',
                        header: {
                            'content-type': 'application/json'
                        },
                        data: {
                            user_id: that.data.userid,
                            task_id: that.data.taskid
                        },
                        success: (res) => {
                            that.set({
                                isfinished: true,
                                buttonleft: '已完成'
                            })
                            wx.showToast({
                              title: '确认成功',
                              icon: 'success',
                              duration: 1000
                            })
                        }
                    })
                }
            }
        },
        RightSubbmit() {
            var that = this;
            if (this.data.buttonright == '已打款') {          
                wx.showToast({
                  title: '已打款',
                  icon: 'success',
                  duration: 1000
                })
            }
            else if (this.data.buttonright == '打款') {
              if (!this.data.isfinished) {    
                wx.showToast({
                  title: '用户还未完成',
                  icon: 'fail',
                  duration: 1000
                })
              }
              else {
                wx.request({
                  url: that.data.reqeusturl + 'task/pay',
                  method: 'POST',
                  header: {
                    'content-type': 'application/json'
                  },
                  data: {
                    user_id: that.data.userid,
                    task_id: that.data.taskid
                  },
                  success: (res) => {
                    that.set({
                        ispaid: true,
                        buttonright: '已收款'
                    })
                  }
                })
              }
            }
        },
        ShowQueryMessage() {
            wx.navigateTo({
                url: 'queryInfo?user_id=' + this.user_id + '&task_id=' + this.task_id + '&template_id=' + this.temp_id
            })
        }
    }
});
