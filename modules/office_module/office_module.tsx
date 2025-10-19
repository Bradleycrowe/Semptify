import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

/*
  Semptify Office Module
  - Join/Host Certified Room, Notary Station, Organizer Workspace
  - Document Dropzone with immediate SHA-256 hashing and upload
  - Live Review with time-stamped annotations
  - Multi-AI orchestration starter button
  - Syncs with law_notes_module via events endpoint

  Drop this file into your React frontend under modules/office_module/
  and wire the route /office to render <OfficeModule />.
*/

type RoomType = "certified" | "notary" | "open";

export default function OfficeModule() {
  const [rooms, setRooms] = useState<any[]>([]);
  const [currentRoom, setCurrentRoom] = useState<string | null>(null);
  const [roomType, setRoomType] = useState<RoomType>("open");
  const [uploading, setUploading] = useState(false);
  const [documents, setDocuments] = useState<any[]>([]);
  const [annotationText, setAnnotationText] = useState("");
  const [aiJobId, setAiJobId] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    fetchRooms();
    fetchDocuments();
  }, []);

  async function fetchRooms() {
    try {
      const res = await axios.get("/api/rooms");
      setRooms(res.data || []);
    } catch (e) {
      console.warn("fetchRooms error", e);
    }
  }

  async function fetchDocuments() {
    try {
      const res = await axios.get("/api/documents");
      setDocuments(res.data || []);
    } catch (e) {
      console.warn("fetchDocuments error", e);
    }
  }

  async function createRoom() {
    try {
      const res = await axios.post("/api/rooms/create", {
        type: roomType,
        expires_in: 60 * 60,
      });
      fetchRooms();
      setCurrentRoom(res.data.id);
    } catch (e) {
      console.warn("createRoom error", e);
    }
  }

  async function getJoinToken(roomId: string) {
    const res = await axios.post(`/api/rooms/${roomId}/token`);
    return res.data.token;
  }

  async function joinRoom(roomId: string) {
    const token = await getJoinToken(roomId);
    // open Jitsi/embedded WebRTC room URL with token
    const url = `/video/?room=${roomId}&token=${token}`;
    window.open(url, "_blank");
  }

  async function handleFileSelect(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);

    // compute SHA-256 in browser
    const arrayBuffer = await file.arrayBuffer();
    const hashBuffer = await crypto.subtle.digest("SHA-256", arrayBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, "0")).join("");

    try {
      // upload using multipart with pre-signed URL pattern
      const init = await axios.post("/api/documents/upload/init", {
        filename: file.name,
        size: file.size,
        sha256: hashHex,
      });
      const { uploadUrl, id } = init.data;
      await fetch(uploadUrl, { method: "PUT", body: file });
      await axios.post(`/api/documents/${id}/complete`);
      setUploading(false);
      fetchDocuments();
    } catch (err) {
      console.error("upload error", err);
      setUploading(false);
    }
  }

  async function lockDocument(docId: string) {
    await axios.post(`/api/documents/${docId}/lock`);
    fetchDocuments();
  }

  async function addAnnotation(docId: string) {
    await axios.post(`/api/documents/${docId}/annotate`, {
      text: annotationText,
      timecode: new Date().toISOString(),
    });
    setAnnotationText("");
    fetchDocuments();
  }

  async function orchestrateWithAI(selectedDocIds: string[]) {
    try {
      const res = await axios.post("/api/ai/orchestrate", {
        requester: "web_client",
        input_refs: selectedDocIds,
        ais: [
          { name: "summarizer", role: "summarizer" },
          { name: "draftr", role: "drafter" },
          { name: "redteam", role: "red-teamer" }
        ],
        strategy: "synthesize",
        approval_required: true
      });
      setAiJobId(res.data.job_id);
    } catch (e) {
      console.warn("orchestrate error", e);
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h3>Semptify Office</h3>

      <section>
        <h4>Rooms</h4>
        <select value={roomType} onChange={e => setRoomType(e.target.value as RoomType)}>
          <option value="open">Organizer Workspace</option>
          <option value="certified">Certified Counsel Room</option>
          <option value="notary">Notary Station</option>
        </select>
        <button onClick={createRoom}>Create Room</button>
        <div>
          {rooms.map(r => (
            <div key={r.id} style={{ border: "1px solid #ddd", padding: 8, marginTop: 8 }}>
              <strong>{r.type}</strong> {r.id}
              <button onClick={() => joinRoom(r.id)} style={{ marginLeft: 8 }}>Join</button>
            </div>
          ))}
        </div>
      </section>

      <hr />

      <section>
        <h4>Document Center</h4>
        <input type="file" ref={fileInputRef} onChange={handleFileSelect} />
        {uploading && <div>Uploading and hashing…</div>}
        <div style={{ marginTop: 12 }}>
          {documents.map(d => (
            <div key={d.id} style={{ border: "1px solid #eee", padding: 8, marginTop: 8 }}>
              <div><strong>{d.filename}</strong> — <small>{d.sha256}</small></div>
              <div>
                <button onClick={() => lockDocument(d.id)}>Timestamp & Lock</button>
                <button onClick={() => window.open(`/files/${d.id}`)} style={{ marginLeft: 8 }}>View</button>
              </div>
            </div>
          ))}
        </div>
      </section>

      <hr />

      <section>
        <h4>Live Review</h4>
        <textarea value={annotationText} onChange={e => setAnnotationText(e.target.value)} placeholder="Time-stamped note" />
        <button onClick={() => addAnnotation(documents[0]?.id)}>Add Annotation</button>
      </section>

      <hr />

      <section>
        <h4>Cross-AI Workspace</h4>
        <div>
          <button onClick={() => orchestrateWithAI(documents.slice(0,3).map(d => d.id))}>Start 3-AI Orchestration</button>
        </div>
        {aiJobId && <div>AI job created {aiJobId} — requires human approval before export</div>}
      </section>
    </div>
  );
}
