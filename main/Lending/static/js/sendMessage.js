import { getCookie } from './getCookie.js';
export async function sendMessage(message, chat_id, value, name) {
    let status = true;
    try {
        const response = await fetch('/api/send-message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                message: message, 
                chat_id: chat_id,  
                value: value,
                name: name
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
