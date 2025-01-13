export async function hashProcess(number) {
    const encoder = new TextEncoder();
    const data = encoder.encode(number);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashedStr = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
    return hashedStr;
}