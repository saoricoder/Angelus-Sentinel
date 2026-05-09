"use client";

import { Activity, ShieldAlert, Clock, Bell, Hospital, User, CheckCircle, AlertTriangle, Zap, Loader2 } from "lucide-react";
import { useState, useEffect } from "react";
import SentinelChat from "@/components/SentinelChat";
import ActivityLog from "@/components/ActivityLog";

export default function Home() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [simulating, setSimulating] = useState(false);

  const fetchAlerts = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/alerts");
      const data = await response.json();
      setAlerts(data);
    } catch (error) {
      console.error("Error fetching alerts:", error);
    }
  };

  const fetchLogs = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/notifications");
      const data = await response.json();
      setLogs(data);
    } catch (error) {
      console.error("Error fetching logs:", error);
    }
  };

  useEffect(() => {
    fetchAlerts();
    fetchLogs();
    const interval = setInterval(() => {
      fetchAlerts();
      fetchLogs();
    }, 5000); 
    return () => clearInterval(interval);
  }, []);

  const simulateWebhook = async () => {
    setSimulating(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/webhook/emergency", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patient_id: "0912345678",
          hospital_id: "HOSP-METROPOLITANO",
          emergency_type: "Pérdida de conciencia repentina",
          operator_name: "SISTEMA_WEBHOOK"
        })
      });
      
      if (response.ok) {
        // Forzar actualización inmediata de los componentes
        setTimeout(async () => {
          await fetchAlerts();
          await fetchLogs();
        }, 500);
      }
    } catch (error) {
      console.error("Simulación fallida:", error);
    } finally {
      setTimeout(() => setSimulating(false), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-12">
      {/* Navigation */}
      <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white shadow-lg shadow-primary/20">
                <ShieldAlert size={24} />
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold font-heading leading-none text-slate-800 tracking-tighter">ANGELUS</span>
                <span className="text-[10px] font-bold text-primary tracking-widest uppercase opacity-80">Sentinel Console</span>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <button 
                onClick={simulateWebhook}
                disabled={simulating}
                className={`${
                  simulating ? 'bg-emerald-500' : 'bg-amber-500 hover:bg-amber-600'
                } text-white px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition-all shadow-lg active:scale-95 disabled:opacity-90`}
              >
                {simulating ? <CheckCircle className="animate-bounce" size={14} /> : <Zap size={14} />}
                {simulating ? "PROCESANDO EVENTO..." : "SIMULAR WEBHOOK (TEMA 4)"}
              </button>
              
              <div className="badge-online">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                Sistema Monitoreo Activo
              </div>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-140px)]">
          
          {/* Panel Izquierdo: Feed de Alertas (3 cols) */}
          <div className="lg:col-span-3 flex flex-col gap-4 overflow-hidden bg-white/50 p-4 rounded-3xl border border-slate-200 shadow-inner">
            <div className="flex items-center justify-between px-2">
              <h2 className="font-bold text-slate-800 uppercase tracking-widest text-[10px] flex items-center gap-2">
                <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
                Monitoreo de Ingresos
              </h2>
              <span className="text-[10px] font-black text-primary bg-primary/10 px-2 py-0.5 rounded-full">{alerts.length} EVENTOS</span>
            </div>
            
            <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar pb-10">
              {alerts.length === 0 && (
                <div className="text-center py-10 opacity-40 italic text-sm">Escaneando ingresos...</div>
              )}
              {alerts.map((alert) => (
                <div key={alert.id} className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm hover:shadow-md hover:border-primary/40 transition-all group">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex flex-col">
                      <span className="text-[10px] font-bold text-slate-400 mb-1">{new Date(alert.timestamp).toLocaleString()}</span>
                      <h4 className="font-bold text-slate-800 text-base">{alert.patient_name}</h4>
                    </div>
                    <span className={`px-2 py-1 rounded-lg text-[9px] font-black uppercase text-white shadow-sm`} style={{ backgroundColor: alert.analysis?.triage_color || '#ccc' }}>
                      {alert.analysis?.triage_priority || 'PENDIENTE'}
                    </span>
                  </div>
                  
                  <div className="flex items-center gap-2 text-[11px] text-slate-500 font-bold mb-3 bg-slate-50 p-2 rounded-lg">
                    <Hospital size={12} className="text-primary" /> 
                    {alert.hospital_id}
                  </div>

                  <p className="text-[11px] text-slate-600 line-clamp-2 mb-4 italic">
                    "{alert.analysis?.reasoning || 'Procesando análisis...'}"
                  </p>

                  <div className="flex items-center justify-between border-t border-slate-50 pt-3">
                    <div className={`text-[11px] font-black flex items-center gap-1 ${alert.analysis?.decision === 'APROBADO' ? 'text-emerald-600' : 'text-amber-600'}`}>
                      {alert.analysis?.decision === 'APROBADO' ? <CheckCircle size={14} /> : <AlertTriangle size={14} />}
                      {alert.analysis?.decision || 'REVISIÓN'}
                    </div>
                    <span className="text-[10px] font-mono text-slate-300 bg-slate-50 px-1.5 rounded">ID: {alert.patient_id}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Panel Central: Angelus Sentinel Chat (6 cols) */}
          <div className="lg:col-span-6 flex flex-col">
            <SentinelChat />
          </div>

          {/* Panel Derecho: Log de Actividad y Notificaciones (3 cols) */}
          <div className="lg:col-span-3 flex flex-col h-full overflow-hidden">
            <ActivityLog logs={logs} />
          </div>

        </div>
      </main>
    </div>
  );
}
