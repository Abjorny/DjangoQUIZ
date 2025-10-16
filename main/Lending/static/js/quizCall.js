import { sendMessage } from './sendMessage.js'; 

$(document).ready(function () {
    const inputData = {}; 
    const $paramsElement = $('#script-params'); 
    const chatId = $paramsElement.data('chat-id');
    
    let page = 1;
    let inputDataString = `${cleanTitle}\n${cleanTitleSlider}\n\n`;
    // ======= success popup =======
function showSuccessPopup() {
	const popupSuccess = document.getElementById("popup-success");
	if (!popupSuccess) return;

	// показываем попап
	popupSuccess.classList.add("popup-success--show");

	// блокируем скролл
	document.body.classList.add("lock");

	// авто-скрытие через 3 секунды
	setTimeout(() => {
		popupSuccess.classList.remove("popup-success--show");
		document.body.classList.remove("lock"); // разблокируем скролл
		location.reload();
	}, 3000);
}



    function checkFields(currentFrame) {
        const inputs = currentFrame.find("input, textarea, select");
        inputs.each(function () {
            const associatedSpan = $(this).siblings(".form-number__invalid");
            const associatedSpanContacnt = $(this).siblings(".adress-form__invalid");
            associatedSpan.removeClass("active-error");
            associatedSpanContacnt.removeClass("active-error");
        });
    }

    $(".quiz__slide input, .quiz__slide textarea, .quiz__slide select").on("input", function () {
        const currentFrame = $(this).closest(".quiz__slide");
        checkFields(currentFrame);
    });
    
    $(".quiz-button-prev").on("click", function (e) {
        page -= 1;
    });

    $(".quiz-button-next").on("click", function (e) {
        const currentButton = $(this);
        const currentFrame = currentButton.closest(".quiz__slide");
        if (currentFrame.length) {
            const inputs = currentFrame.find("input, textarea, select");
        
            inputs.each(function () {
                const name = $(this).attr("name");
                const type = $(this).attr("type");
                let value = $(this).val();
        
                if (type === "radio") {
                    if ($(this).is(":checked")) {
                        inputData[name] = value;
                    }
                } else {
                    if (name) inputData[name] = value;
                }
            });
        }
        

        page += 1;
        if (page > $(".quiz-button-next").length) {
            for (const [key, value] of Object.entries(inputData)) {
                inputDataString += `${key}: <strong>${value}</strong>\n`;
            }
            $("#quizButtonSet").click();
        }
        console.log(inputData)

    });

    $('#button-end-model-quiz').on('click', async function() {
        var contactForm = $('#contact-form');  
        var name = contactForm.attr('placeholder');  
        var value = contactForm.val();       

        if (value) {
            $(this).prop('disabled', true);
            inputDataString += name + " : " + value + "\n"; 
            await sendMessage(inputDataString, chatId);
            showSuccessPopup();
            
        }
    });
});
