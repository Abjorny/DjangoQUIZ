$(document).ready(function () {

    $("#quiz-title-model").html(quizzes.title);
    $("#quiz-title-model-end").html(quizzes.endFrame.title);
    $("#button-end-model-quiz").html(quizzes.endFrame.text_button);

    $("#label-tg").html(function (index, html) {
        return html.replace(/text/g, quizzes.endFrame.text_telegram);
    });
    $("#label-whatsapp").html(function (index, html) {
        return html.replace(/text/g, quizzes.endFrame.text_whatsapp);
    });

    $("#label-phone").text(quizzes.endFrame.text_phone)


    function getRadioModel(questTitle, inputs, ids) {
        const radioItems = inputs.map((input, index) => `
    <div class="radio-form__item">
        <input data-question="1" type="radio" id="point_${index + 1}" name="${questTitle}" value="${input.text}" ${index === 0 ? 'checked' : ''}>
        <label for="point_${index + 1}">${input.text}</label>
    </div>
    `).join('');




        return `
    <div class="quiz__slide swiper-slide">
    <div class="quiz__content">
    <div class="quiz__caption">
    <b>${questTitle}</b>
    </div>
    <form class="radio-form" action="#">
    <div class="radio-form__items">
        ${radioItems}
    </div>
    <div class="buttons-quiz">
        <button type="button" class="quiz-button-prev"></button>
        <button disabled id = "${ids ? ids : ''}" type="button" class="quiz-button-next" style = "background-color: ${accentColor}">Далее</button>
    </div>
    </form>
    </div>
    </div>
    `;
    }

    function getDropdownModel(questTitle, inputs, ids) {
        const formItems = inputs.map((input, index) => `
    <div class="form-size__item">
        <label for="${index + 1}">${input.text}:</label>
        <div class="form-number">
            <input data-question="1"  type="text" id="${index + 1}" name="${input.text}" placeholder="${input.placeholder}" value="">
            <span class="form-number__invalid invalid">Не заполнено поле</span>
        </div>
        <span class="form-size__text">${input.type_text ? input.type_text : ''}</span>
    </div>
    `).join('');

        return `
    <div class="quiz__slide swiper-slide">
        <div class="quiz__content">
            <div class="quiz__caption">
                <b>${questTitle}</b>
            </div>
            <form class="form-size" action="#">
                <div class="form-size__items">
                    ${formItems}
                </div>
                <div class="buttons-quiz">
                    <button type="button" class="quiz-button-prev"></button>
                    <button disabled id="${ids ? ids : ''}" type="button" class="quiz-button-next" style = "background-color: ${accentColor}" >Далее</button>
                </div>
            </form>
        </div>
    </div>
    `;
    }

    function getInputModel(questTitle, inputs, ids) {
        const inputFields = inputs.map((input, index) => `
    <div class="adress-form__item">
    <label for="${index + 1}">${input.text}</label>
    <div class="adress-form__adress">
    <input  data-question="1"  type="text id="${index + 1}" name="${input.text}" placeholder="${input.placeholder}" >
    <span class="adress-form__invalid invalid">Не заполнено поле</span>
    </div>
    </div>
    `).join('');

        return `
    <div class="quiz__slide swiper-slide">
    <div class="quiz__content">
    <div class="quiz__caption">
    <b>${questTitle}</b>
    </div>
    <form class="adress-form" action="#">
    <div class="adress-form__items">
        ${inputFields}
    </div>
    <div class="buttons-quiz">
        <button type="button" class="quiz-button-prev"></button>
        <button disabled id = "${ids ? ids : ''}" type="button" class="quiz-button-next" style = "background-color: ${accentColor}" >Далее</button>
    </div>
    </form>
    </div>
    </div>
    `;
    }


    const containerModal = $('#container-model-quiz')

    quizzes.questions.map(function (question, index) {
        if (index === 0) {
            if (question.question_type === "radio") {
                containerModal.prepend(getRadioModel(question.text, question.inputs_data, 'btn-next'));
            }
            else if (question.question_type === "dropdown") {
                containerModal.prepend(getDropdownModel(question.text, question.inputs_data, 'btn-next'));
            }
            else {
                containerModal.prepend(getInputModel(question.text, question.inputs_data, 'btn-next'));
            }
        }

        else if (question.question_type === "radio") {
            containerModal.prepend(getRadioModel(question.text, question.inputs_data));
        }
        else if (question.question_type === "dropdown") {
            containerModal.prepend(getDropdownModel(question.text, question.inputs_data));
        }
        else {
            containerModal.prepend(getInputModel(question.text, question.inputs_data));
        }
    });

});