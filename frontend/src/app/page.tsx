"use client";

import { Activity, ShieldAlert, Clock, Bell, Hospital, User, CheckCircle, AlertTriangle } from "lucide-react";
import { useState, useEffect } from "react";

export default function Home() {
  const [alerts, setAlerts] = useState<any[]>([]);

  // Simulación de alertas recibidas por el webhook
  useEffect(() => {
    const mockAlerts = [
      {
        id: 1,
        patient: "Miguel Herrera",
        hospital: "Hospital Metropolitano",
        time: "10:45 AM",
        status: "Validado",
        decision: "APROBADO",
        type: "Emergencia Cardiaca"
      },
      {
        id: 2,
        patient: "Elena Paz",
        hospital: "Clínica Kennedy",
        time: "11:20 AM",
        status: "En Proceso",
        decision: "REVISIÓN",
        type: "Traumatismo"
      }
    ];
    setAlerts(mockAlerts);
  }, []);

  return (
    <div className="min-h-screen bg-background pb-12">
      {/* Navigation */}
      <nav className="bg-surface border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white shadow-lg shadow-primary/20">
                <ShieldAlert size={24} />
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold font-heading leading-none">ANGELUS</span>
                <span className="text-[10px] font-bold text-primary tracking-widest uppercase opacity-80">Sentinel</span>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="badge-online">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                Sistema Activo
              </div>
              <button className="p-2 text-slate-500 hover:text-primary transition-colors">
                <Bell size={20} />
              </button>
              <div className="w-8 h-8 bg-slate-200 rounded-full border-2 border-primary/20 overflow-hidden">
                 <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Angelus" alt="Avatar" />
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">Panel del Centinela</h1>
          <p className="text-slate-500">Gestión de alertas y validaciones en tiempo real para el ecosistema hospitalario.</p>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card p-6 bg-surface shadow-sm border border-slate-200">
            <div className="flex justify-between items-start mb-4">
              <div className="p-2 bg-indigo-50 text-primary rounded-lg">
                <Activity size={24} />
              </div>
              <span className="text-xs font-bold text-green-600 bg-green-50 px-2 py-1 rounded">+12%</span>
            </div>
            <p className="text-slate-500 text-sm font-semibold uppercase tracking-wider mb-1">Validaciones Hoy</p>
            <h3 className="text-4xl font-bold">24</h3>
          </div>

          <div className="card p-6 bg-surface shadow-sm border border-slate-200">
            <div className="flex justify-between items-start mb-4">
              <div className="p-2 bg-red-50 text-red-600 rounded-lg">
                <AlertTriangle size={24} />
              </div>
            </div>
            <p className="text-slate-500 text-sm font-semibold uppercase tracking-wider mb-1">Alertas Críticas</p>
            <h3 className="text-4xl font-bold text-red-600">2</h3>
          </div>

          <div className="card p-6 bg-surface shadow-sm border border-slate-200">
            <div className="flex justify-between items-start mb-4">
              <div className="p-2 bg-amber-50 text-amber-600 rounded-lg">
                <Clock size={24} />
              </div>
            </div>
            <p className="text-slate-500 text-sm font-semibold uppercase tracking-wider mb-1">Tiempo de Respuesta</p>
            <h3 className="text-4xl font-bold">1.2s</h3>
          </div>
        </div>

        {/* Recent Alerts */}
        <section className="bg-surface rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
            <h2 className="font-bold text-lg">Ingresos Recientes</h2>
            <button className="text-sm font-bold text-primary hover:underline">Ver todo</button>
          </div>
          
          <div className="divide-y divide-slate-100">
            {alerts.length > 0 ? (
              alerts.map((alert) => (
                <div key={alert.id} className="px-6 py-6 hover:bg-slate-50/50 transition-colors flex flex-wrap gap-4 items-center justify-between">
                  <div className="flex items-center gap-4 min-w-[200px]">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center ${alert.decision === 'APROBADO' ? 'bg-green-100 text-green-600' : 'bg-amber-100 text-amber-600'}`}>
                      <User size={24} />
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-900">{alert.patient}</h4>
                      <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
                        <Hospital size={12} /> {alert.hospital}
                      </div>
                    </div>
                  </div>

                  <div className="flex-1 min-w-[150px]">
                    <p className="text-xs font-bold text-slate-400 uppercase mb-1">Tipo de Ingreso</p>
                    <p className="text-sm font-semibold text-slate-700">{alert.type}</p>
                  </div>

                  <div>
                    <p className="text-xs font-bold text-slate-400 uppercase mb-1">Decisión Angelus</p>
                    <div className={`flex items-center gap-1 text-sm font-bold ${alert.decision === 'APROBADO' ? 'text-green-600' : 'text-amber-600'}`}>
                      {alert.decision === 'APROBADO' ? <CheckCircle size={16} /> : <AlertTriangle size={16} />}
                      {alert.decision}
                    </div>
                  </div>

                  <div className="text-right">
                    <p className="text-xs font-bold text-slate-400 uppercase mb-1">Hora</p>
                    <p className="text-sm font-semibold text-slate-700">{alert.time}</p>
                  </div>
                </div>
              ))
            ) : (
              <div className="py-20 text-center">
                <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-4 text-slate-300">
                  <Activity size={32} />
                </div>
                <p className="text-slate-400 font-medium">Escaneando red en busca de ingresos...</p>
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
