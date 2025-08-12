export async function chat({ baseUrl, apiKey, messages, model, stream=false, response_format, tools }: any) {
  const r = await fetch(`${baseUrl}/v1/chat`, {
    method: "POST",
    headers: { "Content-Type":"application/json", "Authorization": `Bearer ${apiKey}` },
    body: JSON.stringify({ messages, model, stream, response_format, tools })
  });
  if (!r.ok) {
    throw new Error(await r.text());
  }
  return await r.json();
}
