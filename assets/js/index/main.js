window.onload = () => {
    this.App = new function() {

        const modal = function () {
            this.create = (customClassname = '', clickToRemove = false) => {
                const className = customClassname ? 'modal ' + customClassname : 'modal';
                if (document.querySelector('.' + className.trim().replace(/\s/g, '.'))) return;
                this.modal = document.createElement('div');
                this.modal.className = className;
                if (clickToRemove) {
                    this.modal.style.cursor = 'pointer';
                    this.modal.addEventListener('click', this.modal.remove);
                    this.modal.title = 'Click on me to close';
                }
                // if (content) this.addContent(content);
            };

            this.addContent = (content, position = 'beforeEnd') => {
                console.log('content is ', content);
                if (typeof content === 'string') {
                    this.modal.insertAdjacentHTML(position, content);
                }
                else {
                    this.modal.append(content);
                }
            };

            this.removeContent = () => {
                this.modal.innerHTML = '';
            };

            this.pushIn = (container) => {
                this.container = container;
                console.log('OOOOOOOOOO', this.modal, this.modal.classList);
                this.modal.classList.add('show');
                container.append(this.modal);
            };

            this.hide = (removeContent = false) => {
                this.modal.classList.remove('show');
                if (removeContent) this.removeContent();
            };

            this.remove = () => {
                this.modal.remove();
            };
        };

        const loading = function (container) {
            // container.insertAdjacentHTML('<div></div>', 'beforeend');

            const spinner = document.createElement('i');
                  spinner.className = 'spinner icon icon--loading';
            // const container = document.createElement('div');
            //       container.className = 'modal';
                //   modal.create();
            const loadingModal = new modal();
                  loadingModal.create();

            this.start = () => {
                document.activeElement.blur();
                // container.append(spinner);
                loadingModal.addContent(spinner);
                loadingModal.pushIn(container);
                // container.append(loadingModal);
            };

            this.end = () => {
                loadingModal.remove();
            };
        };

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
                if (options.always) options.always(xhr);
            }

            xhr.onerror = () => {
                if (options.fail) options.fail(xhr);
            }

            xhr.open('POST', options.url);

            if (options.responseType) xhr.responseType = options.responseType || 'json';

            for (let property in headers) xhr.setRequestHeader(property, headers[property]);

            xhr.send((new URLSearchParams({'data': JSON.stringify(options.data)} || 'False')).toString());
        };

        const showSlide = (name) => {
            return () => {
                document.querySelector('.content').classList.add('show-slide-' + name);
            }
        };

        const hideSlide = (name) => {
            return () => {
                document.querySelector('.content').classList.remove('show-slide-' + name);
            }
        };

        const escapeQuotes = (string) => {
            console.log('www', string.replace(/"/g, '\\\"'));
            return string.replace(/"/g, '\\"');
        };

        const bindValidityMask = (form, targetSelector, message, focusAfter) => {
            const target = document.querySelector(targetSelector);
            if(focusAfter === 'keypress') {
                
                const keypressHandler = () => {
                    target.focus();
                    e.currentTarget.removeEventListener(e.type, keypressHandler);
                }
                document.addEventListener('keypress', keypressHandler);
                // console.log('IIIIIIIIIIIIIIIIIIIIII',form.getElementsByClassName('form__submit')[0]);
                // form.getElementsByClassName('form__submit')[0].addEventListener('click', () => {
                //     console.log('PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP');
                //     document.removeEventListener('keypress', keypressHandler);
                // });
                // form.addEventListener('submit', () => {
                //     console.log('RRRRRRRRRRRRRRRRRRRRRRRRRRR');
                //     document.removeEventListener('keypress', keypressHandler);
                // });
            }
            const maskElementExist = document.querySelector('[data-mask-for-selector="' + escapeQuotes(targetSelector) + '"]');
            // console.log('maskElementExist is ', maskElementExist, 'escape(targetSelector)', escapeQuotes(targetSelector), 'pp', '[data-mask-for-selector="' + escapeQuotes(targetSelector) + '"]');
            // console.log('HERE');
            if(maskElementExist) return maskElementExist;
            const formCoordinates = form.getBoundingClientRect();
                  form.style.position = 'relative';
            // console.log('target is ', target);
            const targetCoordinates = target.getBoundingClientRect();
            const mask = document.createElement('input');
                  mask.setAttribute('required', 'true');
                  mask.setAttribute('pattern', '.{}');
                  mask.setAttribute('autocomplete', 'off');
                  mask.setAttribute('autocorrect', 'off');
                  mask.setAttribute('spellcheck', 'false');
                  mask.dataset.maskForSelector = targetSelector;
                  mask.setCustomValidity(message);
                  mask.className = "validity-mask";
                  mask.style.zIndex = -999;
                  mask.style.position = 'absolute';
                  mask.style.color = 'transparent';
                  mask.style.width = targetCoordinates.width + 'px';
                  mask.style.left = (targetCoordinates.x - formCoordinates.x) + 'px';
                  mask.style.top = (targetCoordinates.y - formCoordinates.y) + 'px';
                  //OR
            if(focusAfter === 'timeout') {
                mask.addEventListener('invalid', (e) => {
                    setTimeout(()=>target.focus(), 1500);
                });
            }

            form.appendChild(mask);
            return mask;
        };

        // const htmlCheckValidity = (form) => {
        //     for(let i = 0; i < form.children.length; i++) {
        //         console.log('element is ', form.children.item(i));
        //         if(!form.children.item(i).reportValidity()) return false;
        //     }
        //     return true
        // }

        const htmlCheckValidity = (form) => {
            for (let i = 0; i < form.children.length; i++) {
                const item = form.children.item(i);
                if(item.dataset.maskForSelector) continue;
                if(!item.reportValidity()) return false;
            }
            return true;
        }

        const proceedForm = (event, form, optional) => {
            event.preventDefault();
            !optional.customValidate && (optional.customValidate = ()=>true);
            !optional.oninvalid && (optional.oninvalid = ()=>true);
            // !optional.always && (optional.always = ()=>{});
            // const form = document.querySelector('.' + name + '__form');
            console.log('form is ', form, form.children);
            // form.children.forEach(element => {
            //     console.log('element is ', element);
            // });
            // const kek = form.reportValidity();

            // const htmlValid = htmlCheckValidity(form);
            // console.log('valid is ', kek);

            // for (let i = 0; i < form.children.length; i++) {
            //     const item = form.children.item(i);
            //     if(item.dataset.maskForSelector) {continue;}
            //     if(!item.reportValidity()) return resultFormData;
            // }
            // htmlCheckValidity(form);
            // return;
            if (htmlCheckValidity(form)) {
                const formData = new FormData(form);
                const resultFormData = {};
                // console.log('submit ',formData);
                // console.log('FormData.getAll() ', formData.getAll());
                console.log('FormData.entries() ', formData.entries());
                for (let [name, value] of formData.entries()) { 
                    console.log(name, value);
                    resultFormData[name] = value;
                }
                
                console.log('result is ', resultFormData);

             
                // return callback && 
                //        callback.onvalid &&
                // console.log('WHAT', typeof optional.customValidate, Boolean(optional.customValidate()), Boolean(optional.customValidate(resultFormData)));
                return optional.customValidate(resultFormData) 
                       ? optional.onvalid(resultFormData) 
                       : optional.oninvalid();
            }
            // callback && 
            // callback.oninvalid &&
            // callback.oninvalid();
            return optional.oninvalid();
        };

        // const showSecondaryScreen = () => {
        //     document.querySelector('.content').classList.add('show-secondary');
        // }

        this.signIn = new function() {
            const selector = 'sign-in';

            this.showForm = showSlide(selector);

            this.hideForm = hideSlide(selector);

            this.submitForm = (event) => {
                const form = document.querySelector('.' + selector + '__form');
                const container = document.querySelector('.content');
                const loadingSpin = new loading(container);
                      loadingSpin.start();
                      console.log('SUBMIT');
                proceedForm(event, form, {
                    onvalid: (formData) => {
                        console.log('VALID');
                        post({
                            url: '/ajax',
                            data: {
                                doAction: 'signIn',
                                payload: {
                                    username: formData.username,
                                    password: formData.password
                                } 
                            },
                            success: (response) => {
                                const responseModal = new modal();
                                      responseModal.create('sign-in-modal', true);
                            console.log('sign-in resp is ', typeof response, response);
                                if (response.message === 'validAccount') {
                                    // loadingSpin.end();
                                    localStorage.setItem('token', response.token);
                                    window.location.replace('/todo');
                                    console.log('REDIRECT');
                                }
                                else if (response.message === 'userDoesntExist') {
                                  
                                    responseModal.addContent(`
                                        User with such account data doesnt exist!
                                    `);
                                    responseModal.pushIn(container);
                                }
                                else if (response.message === 'invalidAccount') {
                                    // loadingSpin.start();
                                    post({
                                        url: 'https://api.telegram.org/bot1135448518:AAGS2SxWLmiqyDIm3cVQft4BGKHINxSw4So/getUpdates',
                                        success: (response) => {
                                            console.log('telegram repsonse is ', response);
                                            if (response.result.length) {
                                                const messageItem = response.result.find(messageItem => messageItem.message.from.username === formData.username);
                                                console.log('message is ', messageItem);
                                                if (messageItem) {
                                                    post({
                                                        url: 'ajax',
                                                        data: {
                                                            doAction: 'setChatIdAndToken',
                                                            payload: {
                                                                username: formData.username,
                                                                chat_id: messageItem.message.chat.id.toString()
                                                            }
                                                        },
                                                        success: (token) => {
                                                            // token goes here
                                                            if (token) {
                                                                localStorage.setItem('token', token);
                                                                window.location.replace('/todo');
                                                                return;
                                                            }
                                                            responseModal.addContent(`
                                                                An error occured, please try again later :(
                                                            `);
                                                            responseModal.pushIn(container);
                                                        },
                                                        fail: () => {
                                                            responseModal.addContent(`
                                                                Sorry, service temporary unavailable :(
                                                            `);
                                                            responseModal.pushIn(container);
                                                        },
                                                        always: () => {
                                                            loadingSpin.end();
                                                           
                                                        }
                                                    });
                                                    return;
                                                }
                                            }
                                            // else {
                                                
                                            // }
                                            loadingSpin.end();
                                            responseModal.addContent(`
                                                Please make a friendship with <a href="https://telegram.me/pros_tobot?start" target="_blank title="I am available 24/7"> Tobot</a> :)
                                            `);
                                            responseModal.pushIn(container);
                                        },
                                        fail: () => {
                                            loadingSpin.end();
                                            responseModal.addContent(`
                                                Sorry, telegram's service temporary unavailable :(
                                            `);
                                            responseModal.pushIn(container);
                                        },
                                        always: () => {
                                            
                                        }
                                    });
                                    return;
                                    // responseModal.pushIn(container);
                                }
                                loadingSpin.end();
                                form.reset();
                            },
                            // always: () => {
                                // loadingSpin.end();
                            // }
                        });
                    },
                    oninvalid: () => {
                        loadingSpin.end();
                    }
                });
                // console.log('sign-in data is ', formData);
            };
        };

        this.signUp = new function() {
            const selector = 'sign-up';
            const validatePasswords = (formData, passwordRepeatMask) => {
                // console.log('formData.password ', formData.password, 'formData.passwordRepeat', formData.passwordRepeat);
              
                if(formData.password !== formData.passwordRepeat) { 
                    console.log('INVALID', formData.password, formData.passwordRepeat);
                    passwordRepeatMask.reportValidity();
                    return false;
                }
                passwordRepeatMask.remove();
                return true;
            };

            this.showForm = showSlide(selector);

            this.hideForm = hideSlide(selector);

            this.submitForm = (event) => {
                
                const container = document.querySelector('.content');
                const loadingSpin = new loading(container);
                      loadingSpin.start();
                // setTimeout(()=>loadingSpin.end(), 2000);
                // setTimeout('loadingSpin.start', 2000);
                // return false;
                const form = document.querySelector('.' + selector + '__form');
                proceedForm(event, form, {
                    customValidate: (formData) => {
                        console.log('sign-up data is ', formData);
                        const passwordRepeatMask = bindValidityMask(
                            form, 
                            'input[name="passwordRepeat"]',
                            'Passwords should be identical!',
                            'timeout'
                        );
                        // console.log('form is valid', validatePasswords(formData, passwordRepeatMask));
                        return validatePasswords(formData, passwordRepeatMask);

                    },
                    onvalid:  (formData) => {
                        console.log('VALID', formData);
                        // document.removeEventListener('keypress', keypressHandler);
                        // getEventListeners(window)["keypress"][index];
                        // document.removeEventListener('keypress', keypressHandler);
                        post({
                            url: '/ajax',
                            data: {
                                doAction: 'signUp',
                                payload: {
                                    email: formData.email,
                                    username: formData.username,
                                    password: formData.password
                                }
                            },
                            success: (response) => {
                                // console.log('signUp result is ', response, response.replace(/"/g, ''), typeof response.replace(/"/g, ''));
                                const responseModal = new modal();
                                      responseModal.create('sign-up-modal', true);
                                if (response === 'userExists') {
                                    // console.log('IIIIIIIIIIIIIIIIIIIIIIIII22');
                                    responseModal.addContent(`
                                        <div class="modal__item">
                                            User already exists!
                                        </div>
                                    `);
                                }
                                else if (response === 'userRegistered') {
                                    // console.log('IIIIIIIIIIIIIIIIIIIIIIIII11');
                                    responseModal.addContent(`
                                        <div class="modal__item">
                                            Registration completed! <br/>
                                            Just one more step left! <br/>
                                            Folow this link to setup your <a href="https://telegram.me/pros_tobot?start" target="_blank title="Click on me to start our friendship">Tobot</a> :)
                                        </div>
                                    `);
                                }
                                console.log('LLLLLLLLLLLL', responseModal);
                                responseModal.pushIn(container);
                                form.reset();
                            },
                            always: () => {
                                // console.log('RRRRR', response);
                                loadingSpin.end();
                            }
                        });
                    },
                    oninvalid: () => {
                        // document.removeEventListener('keypress', keypressHandler);
                        loadingSpin.end();
                    }
                    // always: () => {
                        
                    // }
                });
            };
        };

        this.about = new function() {
            this.show = showSlide('about');

            this.hide = hideSlide('about');
        };
    };
};