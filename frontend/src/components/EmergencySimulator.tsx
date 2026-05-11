"use client";

import { useState, useEffect } from "react";
import { Send, Hospital, User, Activity, Loader2 } from "lucide-react";

export default function EmergencySimulator() {
  const [patients, setPatients] = useState<any[]>([]);
  const [selectedPatient, setSelectedPatient] = useState("");
  const [emergencyType, setEmergencyType] = useState("Dolor de Pecho");
  const [operatorName, setOperatorName] = useState("Miguel Herrera");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    fetch("/api/patients")
      .then(res => res.json())
      .then(data => {
        setPatients(data);
        if (data.length > 0) setSelectedPatient(data[0].id);
      });
  }, []);

  const triggerWebhook = async () => {
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch("/api/webhook/emergency", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patient_id: selectedPatient,
          hospital_id: "HOSP-CENTRAL-01",
          emergency_type: emergencyType,
          operator_name: operatorName
        })
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error triggering webhook:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card p-6 border-indigo-100 bg-indigo-50/30">
      <div className="flex items-center gap-2 mb-6">
        <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white">
          <Activity size={18} />
        </div>
        <h3 className="text-lg font-bold text-slate-800">Simulador de Emergencia</h3>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Tu Nombre (Operador)</label>
          <input 
            type="text" 
            className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary outline-none"
            placeholder="Ej: Miguel Herrera"
            value={operatorName}
            onChange={(e) => setOperatorName(e.target.value)}
          />
        </div>

        <div>
          <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Paciente</label>
          <select 
            className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary outline-none"
            value={selectedPatient}
            onChange={(e) => setSelectedPatient(e.target.value)}
          >
            {patients.map(p => (
              <option key={p.id} value={p.id}>{p.name} ({p.id})</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Tipo de Emergencia</label>
          <input 
            type="text" 
            className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary outline-none"
            placeholder="Ej: Accidente de tránsito"
            value={emergencyType}
            onChange={(e) => setEmergencyType(e.target.value)}
          />
        </div>

        <button 
          onClick={triggerWebhook}
          disabled={loading}
          className="w-full bg-primary hover:bg-primary-dark text-white font-bold py-2.5 rounded-lg flex items-center justify-center gap-2 transition-all shadow-lg shadow-primary/20 disabled:opacity-50"
        >
          {loading ? <Loader2 className="animate-spin" size={18} /> : <Send size={18} />}
          Lanzar Alerta al Centinela
        </button>
      </div>

      {result && (
        <div className={`mt-6 p-4 rounded-lg border ${result.decision === 'APROBADO' ? 'bg-green-50 border-green-100 text-green-800' : 'bg-amber-50 border-amber-100 text-amber-800'}`}>
          <p className="text-xs font-bold uppercase mb-1">Respuesta de Angelus:</p>
          <p className="text-sm font-medium italic">"{result.reply}"</p>
        </div>
      )}
    </div>
  );
}
