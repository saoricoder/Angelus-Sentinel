"use client";

import { useState, useEffect, useRef } from "react";
import { Send, Activity, User, Bot, Loader2, CheckCircle2, AlertCircle, Shield } from "lucide-react";

interface Message {
  role: "user" | "angelus";
  content: string;
  type?: "QUESTION" | "DISAMBIGUATION" | "RESULT" | "ERROR";
  color?: string;
  options?: { id: string; label: string }[];
}

export default function SentinelChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "angelus",
      content: "Núcleo Angelus activo. Reporte el ingreso del paciente para iniciar el protocolo de validación.",
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [operatorName, setOperatorName] = useState("Saoricoder");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // const scrollToBottom = () => {
  //   messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  // };

  // useEffect(() => {
  //   scrollToBottom();
  // }, [messages]);

  const sendMessage = async (text: string, confirmedId?: string) => {
    if (!text && !confirmedId) return;

    if (text) {
      setMessages(prev => [...prev, { role: "user", content: text }]);
      setInput("");
    }

    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          operator_name: operatorName,
          confirmed_patient_id: confirmedId
        })
      });
      const data = await response.json();
      
      setMessages(prev => [...prev, { 
        role: "angelus", 
        content: data.reply,
        type: data.type,
        color: data.color,
        options: data.options
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: "angelus", 
        content: "Error de conexión con el núcleo central.",
        type: "ERROR"
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card flex flex-col h-full border-indigo-100 bg-white overflow-hidden shadow-2xl">
      {/* Chat Header */}
      <div className="p-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white shadow-sm">
            <Activity size={18} />
          </div>
          <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider">Comando de Entrada Inteligente</h3>
        </div>
        <div className="flex items-center gap-2">
           <input 
            type="text" 
            value={operatorName}
            onChange={(e) => setOperatorName(e.target.value)}
            className="text-[10px] bg-white border border-slate-200 rounded px-2 py-1 font-bold text-slate-500 outline-none focus:ring-1 focus:ring-primary w-24"
            title="Nombre del Operador"
           />
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-[85%] flex gap-3 ${m.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${m.role === "user" ? "bg-slate-200 text-slate-600" : "bg-primary/10 text-primary"}`}>
                {m.role === "user" ? <User size={16} /> : <Bot size={16} />}
              </div>
              <div 
                className={`p-3 rounded-2xl text-sm ${
                  m.role === "user" 
                  ? "bg-primary text-white rounded-tr-none shadow-md" 
                  : "bg-slate-100 text-slate-800 rounded-tl-none border border-slate-200/50"
                }`}
                style={m.color ? { borderLeft: `6px solid ${m.color}`, paddingLeft: '12px' } : {}}
              >
                {m.type === "RESULT" ? (
                  <div className="space-y-3">
                    <div className="flex items-center gap-2 border-b border-slate-200 pb-2">
                      <Shield size={16} className="text-primary" />
                      <span className="font-bold uppercase tracking-tight text-xs">Informe de Validación Angelus</span>
                    </div>
                    <p className="text-sm italic text-slate-600">"{m.content}"</p>
                    <div className="grid grid-cols-2 gap-2 text-[10px]">
                      <div className="bg-white p-2 rounded border border-slate-200">
                        <span className="block text-slate-400 uppercase font-bold">Estado Póliza</span>
                        <span className="text-slate-800 font-bold">ACTIVA</span>
                      </div>
                      <div className="bg-white p-2 rounded border border-slate-200">
                        <span className="block text-slate-400 uppercase font-bold">Triage Clínico</span>
                        <span className="font-bold" style={{ color: m.color }}>{m.type}</span>
                      </div>
                    </div>
                    <div className="bg-emerald-50 p-2 rounded border border-emerald-100 flex items-center gap-2">
                      <CheckCircle2 size={12} className="text-emerald-500" />
                      <span className="text-[10px] text-emerald-700 font-bold">Notificaciones Enviadas Simultáneamente</span>
                    </div>
                  </div>
                ) : (
                  m.content
                )}
                
                {/* Disambiguation Options */}
                {m.type === "DISAMBIGUATION" && m.options && (
                  <div className="mt-3 grid gap-2">
                    {m.options.map(opt => (
                      <button
                        key={opt.id}
                        onClick={() => sendMessage(`Confirmado: ${opt.label}`, opt.id)}
                        className="bg-white hover:bg-primary/5 text-primary border border-primary/20 text-xs font-bold py-2 px-3 rounded-lg transition-colors flex items-center justify-between group"
                      >
                        {opt.label}
                        <CheckCircle2 size={14} className="opacity-0 group-hover:opacity-100 transition-opacity" />
                      </button>
                    ))}
                  </div>
                )}

                {m.type === "ERROR" && (
                  <div className="mt-2 flex items-center gap-1 text-red-500 text-[10px] font-bold uppercase">
                    <AlertCircle size={12} /> Reintento Sugerido
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-100 p-3 rounded-2xl rounded-tl-none border border-slate-200/50 flex items-center gap-2">
              <Loader2 className="animate-spin text-primary" size={16} />
              <span className="text-xs text-slate-400 font-medium italic">Angelus está procesando...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-slate-100 bg-slate-50/30">
        <div className="relative">
          <input
            type="text"
            className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-sm pr-12 focus:ring-2 focus:ring-primary outline-none shadow-sm transition-all"
            placeholder="Escriba el nombre del paciente y la emergencia..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage(input)}
            disabled={loading}
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={loading || !input}
            className="absolute right-2 top-1.5 p-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-all disabled:opacity-50 shadow-md"
          >
            <Send size={18} />
          </button>
        </div>
        <p className="text-[10px] text-slate-400 mt-2 text-center font-medium uppercase tracking-widest">
           Soporte de lenguaje natural activo • Extracción de Entidades IA
        </p>
      </div>
    </div>
  );
}
