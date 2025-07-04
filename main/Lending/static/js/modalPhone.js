import { sendMessage } from './sendMessage.js'; 

const $paramsElement = $('#script-params'); 
const inputName = $('#modal-name');
const inputPhone = $('#modal-phone');
const chatId = $paramsElement.data('chat-id');

inputPhone.on('input', function (e) {
        let value = e.target.value.replace(/\D/g, ''); 
        if (value.length > 11) value = value.substring(0, 11); 
        let formattedValue = '+7 (';
        if (value.length > 1) formattedValue += value.substring(1, 4)
        if (value.length > 4) formattedValue += ') ' + value.substring(4, 7);
        if (value.length > 7) formattedValue += '-' + value.substring(7, 9);
        if (value.length > 9) formattedValue += '-' + value.substring(9, 11); 
        $(e.target).val(formattedValue); 
});

$('#sendMessageButton').on('click', async function() {
    if (inputPhone.val() != '' && inputName.val() != '' && inputPhone.val().replace(/\D/g, '').length == 11) {
        $(this).prop('disabled', true);
        let message = `Номер телефона: ${inputPhone.val()} \nИмя: ${inputName.val()}`;
        try{
             document.getElementById("feedbackButton").click();
        }
        catch{

        }
        await sendMessage(message, chatId);
        location.reload(); 
    }
});