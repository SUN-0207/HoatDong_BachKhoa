odoo.define('ai_web_editor.OpenAIGenerateContentDialog', function (require) {
    'use strict';
    
    var core = require('web.core');
    var Dialog = require('wysiwyg.widgets.Dialog');
    
    var _t = core._t;
    
    const { loadJS } = require('@web/core/assets');

    var OpenAIGenerateContentDialog = Dialog.extend({
        template: 'wysiwyg.widgets.openai.generate.content',
        events: {
            'change .text_options': '_onChangeTextOptions',
            'change .text_length': '_onChangeTextLength',
            'click .copy-button': '_copyToClipboard',
        },
        init: function (parent, options, media) {
            options = options || {};
            
            if (!options.buttons) {
                options.buttons = [];
                options.buttons.push({text: _t("Accept"), classes: "btn-primary", click: function (ev) {
                    this.save(ev);
                }});
                options.buttons.push({text: _t("Preview"), classes: "btn-primary", click: function (ev) {
                    this.preview(ev);
                }});
                options.buttons.push({text: _t("Cancel"), classes: "btn-secondary", close: true});
            }

            this._super(parent, _.extend({}, {
                title: _t("Gợi ý nội dung")
            }, options));

            this.media = media;
            this.selectedText = $(this.media).html() || '';
            this.opanai_api = '';
        },

        willStart: function () {
            return Promise.all([
                this._super(...arguments),
                this._fetchOpenAIapi()
            ]).then(async function(){
                loadJS("/ai_web_editor/static/src/js/lib/clipboard.js")
            });
        },

        _fetchOpenAIapi: async function(){
            const opanai_api = await this._rpc({ 
                model: 'res.config.settings', 
                method: 'get_openai_api_key',
                args: [[]],
            });
            this.opanai_api = opanai_api;
        },

        start: function () {
            var self = this;
            this.opened().then(function () {
                $('#content')[0].innerHTML = self.selectedText;
            });
            return this._super.apply(this, arguments);
        },

        save: function (ev) {
            this._super.apply(this, arguments);

            var content = this.$('#generated_content')[0].innerHTML;
            
            $(this.media).html(content);
            $(this.media).trigger('content_changed');
            this.final_data = this.media;
            return this._super.apply(this, arguments);
        },

        _onChangeTextOptions: function(ev){
            var options = $('input.text_options');
            for (var i = 0; i < options.length; i++) {
                options[i].checked = false;
            }
            ev.target.checked = true;
        },
        _onChangeTextLength: function(ev){
            var options = $('input.text_length');
            for (var i = 0; i < options.length; i++) {
                options[i].checked = false;
            }
            ev.target.checked = true;
        },
        
        preview: async function(ev){
            ev.preventDefault();
            ev.stopPropagation();

            var question = $('#content');
            if (question){
                if( question[0].innerText == '\n' || question[0].innerText.length == 0){
                    question.addClass("error");
                } else{
                    question.removeClass("error");
                }
            }

            if( question[0].innerText == '\n' || question[0].innerText.length == 0){
                return;
            }

            var user_prompt = '';
            var text_options = $('.text_options')
            for (var i = 0; i < text_options.length; i++) {
                if (text_options[i].checked) {
                    user_prompt += text_options[i].value;
                }
            }

            var max_tokens = '';
            var text_length = $('.text_length')
            for (var i = 0; i < text_length.length; i++) {
                if (text_length[i].checked) {
                    max_tokens += text_length[i].value;
                }
            }

            var pre_fix = 'Hoàn thành và sửa lỗi câu sau nếu có, chỉ trả về một câu duy nhất, có nghĩa và ngắn nhất (ưu tiên tên riêng) sao cho phù hợp với trường Đại học Bách khoa - ĐHQG-HCM: ';

            return await this._rpc({
                route: "/fetch_openai_api",
                // params: {
                //     'question': user_prompt.concat(" ",question[0].innerText),
                //     'max_tokens': max_tokens,
                // },
                params: {
                    'question': pre_fix.concat(" ", question[0].innerText),
                    'max_tokens': max_tokens,
                },
            }).then(function (result) {
                $('#generated_content')[0].innerHTML = result.replace(/\n/g, "<br />");
            });
        },
        _copyToClipboard: function(ev) {
            var content = $('#generated_content');
            if (content){
                if( content[0].innerText == '\n' || content[0].innerText.length == 0){
                    content.addClass("error");
                } else{
                    content.removeClass("error");
                }
            }

            if (window.ClipboardJS){
                var clipboard = new ClipboardJS('.copy-button');
                clipboard.on('success', function(e) {
                    console.log(e);
                });
                clipboard.on('error', function(e) {
                    console.log(e);
                });
            }
        },
    });
    
    
    return OpenAIGenerateContentDialog;
});
    