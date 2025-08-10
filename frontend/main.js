
const API = "http://localhost:8000";

document.getElementById("go").onclick = async () => {
  const el = document.getElementById("f");
  if (!el.files || el.files.length === 0) {
    document.getElementById("msg").textContent = "Bir dosya seçin.";
    return;
  }
  const file = el.files[0];
  document.getElementById("msg").textContent = "URL alınıyor...";

  try {
    const r = await fetch(`${API}/presign`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename: file.name, content_type: file.type || "application/octet-stream" })
    });
    const js = await r.json();
    if (!r.ok) throw new Error(js.detail || "presign error");

    document.getElementById("msg").textContent = "Yükleniyor...";

    const put = await fetch(js.url, {
      method: "PUT",
      headers: { "Content-Type": file.type || "application/octet-stream" },
      body: file
    });
    if (!put.ok) throw new Error("upload failed");

    document.getElementById("msg").textContent = "Tamam.";
    document.getElementById("out").innerHTML = `<a href="${js.public_url}" target="_blank">${js.public_url}</a>`;
  } catch (e) {
    document.getElementById("msg").textContent = String(e.message || e);
  }
};
