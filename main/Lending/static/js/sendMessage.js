import { getCookie } from './getCookie.js';
export async function sendMessage(message, chat_id) {
    let status = true;
    try {
        const response = await fetch('https://skidca.ru/api/send-message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                message: message, 
                chat_id: chat_id,  
            }),
        });

        if (response.ok) {
            status = true;
        } else {
            status = false;
        }
    } catch (error) {
        status = false;
    }

    return status;
}
