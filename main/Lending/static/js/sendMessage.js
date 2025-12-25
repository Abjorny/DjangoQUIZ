import { getCookie } from './getCookie.js';

export async function sendMessage(message, chat_id, value, name, quiz) {
    let status = true;

    const params = new URLSearchParams(window.location.search);

    const utmData = {
        utm_source: params.get('utm_source'),
        utm_medium: params.get('utm_medium'),
        utm_campaign: params.get('utm_campaign'),
        utm_term: params.get('utm_term'),
        utm_content: params.get('utm_content'),
    };


    try {
        const response = await fetch('/api/send-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                message,
                chat_id,
                value,
                name,
                quiz,
                utm: utmData, 
            }),
        });

        status = response.ok;
    } catch (error) {
        status = false;
    }

    return status;
}
