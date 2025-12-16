import { getCookie } from './getCookie.js';

export async function sendMessage(message, chat_id, value, name) {
    let status = true;
    const utmContent = new URLSearchParams(window.location.search).get('utm_content');

    const url = utmContent
        ? `/api/send-message/?utm_content=${encodeURIComponent(utmContent)}`
        : '/api/send-message/';

    try {
        const response = await fetch(url, {
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

        status = response.ok;
    } catch (error) {
        status = false;
    }

    return status;
}
