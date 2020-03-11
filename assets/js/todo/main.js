window.onload = () => {
    this.App = new function() {
        console.log('st ', serverTimeMS);
        let localTimeS = parseInt((new Date(serverTimeMS)).getTime() / 1000);

        // this.getT = () => { return time };
        // Ведем учет текущего времени
        (() => {
            setInterval(() => {
                localTimeS += 2;
                console.log('local time is ', localTimeS);

            }, 2000);
        })();

        const post = (options) => {
            const headers = options.requestHeaders || {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            };
            const xhr = new XMLHttpRequest();

            xhr.onload = () => {
                console.log('x is ', xhr);
              
                if (options.success) {
                    // let response = JSON.parse(xhr.response);
                    // if (typeof response === 'string') response = response.replace(/^"|"?$/g, '');
                    options.success(JSON.parse(xhr.response));
                }
            };

            xhr.onloadend = () => {
                if (options.always) options.always(JSON.parse(xhr.response));
            }

            xhr.onerror = () => {
                if (options.fail) options.fail(xhr);
            }

            xhr.open('POST', options.url);

            if (options.responseType) xhr.responseType = options.responseType || 'json';

            for (let property in headers) xhr.setRequestHeader(property, headers[property]);

            xhr.send((new URLSearchParams({'data': JSON.stringify(options.data)} || 'False')).toString());
        };

        const loading = new function() {
            let container;

            this.start = (containerSelector) => {
                container = document.querySelector(containerSelector);
                container.insertAdjacentHTML('beforeend', `
                    <div class="modal show loading">
                        <i class="spinner icon icon--loading"></i>
                    </div>
                `);
            }

            // this.changeContent = (content) => {
            // }

            this.end = () => {
                container.getElementsByClassName('loading')[0].remove();
            };
        };

        this.todo = new function() {
            const generateId = () => {
                return (new Date).getTime().toString();
            };

            const checkRemind = () => {
                const remind = document.querySelector('.remind');
                // const form = document.querySelector('.todo-form');
                // const formData = new FormData(form);

                let date = document.querySelector('.date');
                let time = document.querySelector('.time');

                if (date.value.length || time.value.length) {
                    // if (!date.reportValidity() || !time.reportValidity())  {
                        
                    // }
                    // date.required = time.required = true;
                    if (date.reportValidity() && time.reportValidity()) {
                        const minRemindTresholdS = 300; // 5 minutes
                        const maxRemindTresholdS = 31536000; // 1 year = 365 days
                        const dateArr = date.value.split('.');
                        const dateMDY = ([dateArr[0], dateArr[1]] = [dateArr[1], dateArr[0]], dateArr.join('.')); // Bring to format mm.dd.yyyy fix
                        date = date.value;
                        time = time.value;
                        const remindAtS = parseInt((new Date(`${dateMDY} ${time}`)).getTime() / 1000);
                        const deltaS = remindAtS - localTimeS;
                        console.log('date', date, 'dateMDY', dateMDY, 'time', time, 'remindMS is ', remindAtS, 'deltaS', deltaS);
                        if (deltaS > minRemindTresholdS && deltaS < maxRemindTresholdS) {
                            remind.className = 'todo__column remind valid';
                            return [true, deltaS, `${date} ${time}`, [dateMDY.replace(/\./g, '/'), time]]; // deltaS - через сколько секунд уведомить пользователя
                        }
                    }
                    remind.className = 'todo__column remind invalid';
                    return [false];
                }
                // date.required = time.required = false;
                remind.className = 'todo__column remind';
                return [true];
                // }
                
            };

            this.edit = (todoId) => {
                window.location.href = '/todo?id=' + todoId;
            };

            this.save = (todoId) => {
                loading.start('.container');
                const result = checkRemind();
                if (result[0]) {
                    // post
                    // if delta provided add it to payload
                    const title = document.querySelector('.title').value;
                    const text = document.querySelector('.text').value;
                    const payload = {
                        todoId: todoId,
                        title: title,
                        text: text
                    };

                    if (result[1]) {
                        payload['token'] = localStorage.getItem('token');
                        payload['timeoutS'] = result[1];
                        payload['remindAt'] = result[2];
                        payload['remindAtMDYArray'] = result[3]
                    }

                    post({
                        url: '/ajax',
                        data: {
                            doAction: 'save',
                            payload: payload
                        },
                        success: (response) => {
                            console.log('save response is ', response);
                        },
                        always: () => {
                            loading.end();
                        }
                    });
                }
                else {
                    loading.end();
                }
                // console.log('save formdata is ', );
            };

            this.discard = (todoId) => {
                window.location.reload(true);
            };

            this.delete = (todoId) => {
                loading.start('.container');
            };

            this.deleteAll = () => {

            };

            this.add = () => {
                loading.start('.container');
                const todoId = generateId();
                post({
                    url: '/ajax',
                    data: {
                        doAction: 'create',
                        payload: {
                            token: localStorage.getItem('token'),
                            todoId: todoId
                        }
                    },
                    success: (rowId) => {
                        console.log('response is ', rowId);
                        if (rowId) {
                            const todos = document.querySelector('.todos');
                            todos.insertAdjacentHTML('afterbegin', `
                                <div class="todo">
                                    <span class="todo__item title"></span>
                                    <span class="todo__item text"></span>
                                    <div class="todo__item">
                                        <div class="todo__column remind">
                                            <span class="label">Remind at:</span>
                                            <span class="date"></span>
                                        </div>
                                        <div class="todo__column buttons">
                                            <button class="todo__edit todo-button hover--zoom" title="Edit todo" onclick="App.todo.edit(${todoId});"><i class="icon icon--edit-todo"></i></button>
                                            <button class="todo__delete todo-button hover--zoom" title="Delete todo" onclick="App.todo.delete(${todoId});"><i class="icon icon--delete-todo"></i></button>
                                        </div>
                                    </div>
                                </div>
                            `);
                        }
                    },
                    always: () => {
                        loading.end();
                    }
                });
            };
        };

        (() => {
           
            const token = localStorage.getItem('token');
            console.log('EXECUTED ', token);
            if (!token) {
                window.location.replace('/');
            }
            else {
                post({
                    url: '/ajax',
                    data: {
                        doAction: 'verifyUserToken',
                        payload: {         
                            token: token
                        }
                    },
                    always: (tokenIsValid) => {
                        console.log('token is valid', tokenIsValid, typeof tokenIsValid);
                        if (!tokenIsValid) { 
                            window.location.replace('/');
                        }
                        else {
                            document.querySelector('.modal.loading').remove();
                        }
                        // remove loading modal
                    }
                });
            }
        })();

        // this.preserveServerTime = (ms) => {
        //     serverTime = ms;
        //     this.preserveServerTime = null;
        // };

        // this.getST = () => {
        //     return serverTime;
        // }
    };
};