import React, { useState, useEffect } from 'react';

interface ScheduledTask {
  id: string;
  group_name: string;
  task: string;
  cron: string;
  active: boolean;
  last_run: string | null;
  next_description: string;
  created_at: string;
}

const API = '/scheduler/tasks';

const Scheduler: React.FC = () => {
  const [tasks, setTasks] = useState<ScheduledTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [groups, setGroups] = useState<string[]>([]);
  const [form, setForm] = useState({ group_name: '', cron: '', description: '' });
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const res = await fetch(API);
      const data = await res.json();
      setTasks(data);
    } catch {
      setError('Error cargando tareas programadas');
    } finally {
      setLoading(false);
    }
  };

  const fetchGroups = async () => {
    try {
      const res = await fetch('/groups');
      const data = await res.json();
      setGroups(data.map((g: { name: string }) => g.name));
    } catch {
      /* ignore */
    }
  };

  useEffect(() => {
    fetchTasks();
    fetchGroups();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setSubmitting(true);
    try {
      const res = await fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          group_name: form.group_name,
          cron: form.cron,
          description: form.description,
          task_template: form.description,
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        setFormError(err.detail || 'Error creando tarea');
      } else {
        setForm({ group_name: '', cron: '', description: '' });
        await fetchTasks();
      }
    } catch {
      setFormError('Error de red');
    } finally {
      setSubmitting(false);
    }
  };

  const handleCancel = async (taskId: string) => {
    await fetch(`${API}/${taskId}`, { method: 'DELETE' });
    await fetchTasks();
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 dark:text-white">Scheduler</h1>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-5 mb-8">
        <h2 className="text-lg font-semibold mb-4 dark:text-white">Nueva tarea programada</h2>
        <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Grupo
            </label>
            <select
              value={form.group_name}
              onChange={(e) => setForm({ ...form, group_name: e.target.value })}
              required
              className="w-full rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-3 py-2 text-sm"
            >
              <option value="">Selecciona un grupo...</option>
              {groups.map((g) => (
                <option key={g} value={g}>{g}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Expresion Cron
            </label>
            <input
              type="text"
              value={form.cron}
              onChange={(e) => setForm({ ...form, cron: e.target.value })}
              placeholder="0 9 * * 1-5"
              required
              className="w-full rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-3 py-2 text-sm font-mono"
            />
            <p className="text-xs text-gray-500 mt-1">min hora dia mes dia_semana</p>
          </div>
          <div className="sm:col-span-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Descripcion / Tarea
            </label>
            <input
              type="text"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              placeholder="Descripcion de la tarea automatica"
              className="w-full rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-3 py-2 text-sm"
            />
          </div>
          {formError && (
            <div className="sm:col-span-2 text-red-500 text-sm">{formError}</div>
          )}
          <div className="sm:col-span-2">
            <button
              type="submit"
              disabled={submitting}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded text-sm font-medium disabled:opacity-50"
            >
              {submitting ? 'Guardando...' : 'Programar tarea'}
            </button>
          </div>
        </form>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-700">
            <tr>
              {['ID', 'Grupo', 'Cron', 'Descripcion', 'Estado', 'Ultimo run', 'Accion'].map((h) => (
                <th key={h} className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {loading && (
              <tr><td colSpan={7} className="px-4 py-4 text-center text-gray-400">Cargando...</td></tr>
            )}
            {error && (
              <tr><td colSpan={7} className="px-4 py-4 text-center text-red-400">{error}</td></tr>
            )}
            {!loading && !error && tasks.length === 0 && (
              <tr><td colSpan={7} className="px-4 py-4 text-center text-gray-400">Sin tareas programadas</td></tr>
            )}
            {tasks.map((t) => (
              <tr key={t.id} className="hover:bg-gray-50 dark:hover:bg-gray-750">
                <td className="px-4 py-3 text-xs font-mono text-gray-500">{t.id.slice(0, 8)}</td>
                <td className="px-4 py-3 text-sm dark:text-white">{t.group_name}</td>
                <td className="px-4 py-3 text-sm font-mono dark:text-indigo-300">{t.cron}</td>
                <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-300">{t.next_description}</td>
                <td className="px-4 py-3">
                  <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${
                    t.active
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400'
                  }`}>
                    {t.active ? 'Activa' : 'Inactiva'}
                  </span>
                </td>
                <td className="px-4 py-3 text-xs text-gray-400">{t.last_run || '-'}</td>
                <td className="px-4 py-3">
                  {t.active && (
                    <button
                      onClick={() => handleCancel(t.id)}
                      className="text-red-500 hover:text-red-700 text-xs font-medium"
                    >
                      Cancelar
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Scheduler;
