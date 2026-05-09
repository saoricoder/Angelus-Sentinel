import React from 'react';
import { Activity, Bell, Shield, Hospital, Zap } from 'lucide-react';

interface LogEntry {
  timestamp: string;
  target?: string;
  message: string;
  type?: 'HOSPITAL' | 'INSURANCE' | 'SYSTEM' | 'WEBHOOK';
  status: string;
}

interface ActivityLogProps {
  logs: LogEntry[];
}

const ActivityLog: React.FC<ActivityLogProps> = ({ logs }) => {
  return (
    <div className="flex flex-col h-full bg-slate-900 text-slate-300 font-mono text-[11px] overflow-hidden border-l border-slate-800 shadow-2xl">
      <div className="p-3 border-b border-slate-800 bg-slate-900/50 flex items-center gap-2">
        <Activity size={14} className="text-emerald-500 animate-pulse" />
        <span className="font-bold uppercase tracking-widest text-emerald-500">Log de Actividad del Sistema</span>
      </div>
      
      <div className="flex-1 overflow-y-auto p-3 space-y-3 custom-scrollbar">
        {logs.length === 0 && (
          <div className="text-slate-600 italic text-center mt-10">Esperando eventos del sistema...</div>
        )}
        {logs.map((log, i) => (
          <div key={i} className="border-l-2 border-slate-700 pl-3 py-1 hover:bg-slate-800/50 transition-colors">
            <div className="flex justify-between items-start mb-1">
              <span className="text-[9px] text-slate-500">
                {new Date(log.timestamp).toLocaleTimeString()}
              </span>
              <span className={`px-1.5 py-0.5 rounded text-[8px] font-bold ${
                log.type === 'HOSPITAL' ? 'bg-blue-500/20 text-blue-400' :
                log.type === 'INSURANCE' ? 'bg-purple-500/20 text-purple-400' :
                log.type === 'WEBHOOK' ? 'bg-amber-500/20 text-amber-400' :
                'bg-emerald-500/20 text-emerald-400'
              }`}>
                {log.status}
              </span>
            </div>
            <div className="flex items-center gap-2 mb-1">
              {log.type === 'HOSPITAL' && <Hospital size={10} className="text-blue-400" />}
              {log.type === 'INSURANCE' && <Shield size={10} className="text-purple-400" />}
              {log.type === 'WEBHOOK' && <Zap size={10} className="text-amber-400" />}
              {log.type === 'SYSTEM' && <Bell size={10} className="text-emerald-400" />}
              <span className="font-bold text-slate-100">{log.target || 'Angelus Core'}</span>
            </div>
            <p className="text-slate-400 line-clamp-2 leading-tight">{log.message}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ActivityLog;
