import { Header } from '@/components/layout/Header';
import { ModeSwitcher } from '@/components/layout/ModeSwitcher';
import { ChatContainer } from '@/components/chat/ChatContainer';
import { PromptEditor } from '@/components/prompt/PromptEditor';
import { DeltaMeter } from '@/components/metrics/DeltaMeter';
import { ObjectivesPanel } from '@/components/objectives/ObjectivesPanel';

export default function HomePage() {
  return (
    <div className="min-h-screen p-4 md:p-6">
      <Header />

      <main className="max-w-7xl mx-auto mt-6">
        {/* Top bar with mode switcher and metrics */}
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1">
            <ModeSwitcher />
          </div>
          <div className="md:w-64">
            <DeltaMeter />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left column: Prompt editor and objectives */}
          <div className="lg:col-span-1 space-y-6">
            <PromptEditor />
            <ObjectivesPanel />
          </div>

          {/* Middle column: Chat container */}
          <div className="lg:col-span-2">
            <ChatContainer />
          </div>

          {/* Right column: Metrics and status (optional) */}
          <div className="lg:col-span-3 lg:col-start-1 lg:row-start-2">
            <div className="glass-panel rounded-2xl p-4">
              <h3 className="text-lg font-semibold text-white mb-2">Estado del Sistema</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-3 rounded-xl bg-white/5">
                  <div className="text-sm text-white/50">Conexión</div>
                  <div className="text-success font-bold">● Activa</div>
                </div>
                <div className="text-center p-3 rounded-xl bg-white/5">
                  <div className="text-sm text-white/50">Tokens</div>
                  <div className="text-white font-bold">1,240</div>
                </div>
                <div className="text-center p-3 rounded-xl bg-white/5">
                  <div className="text-sm text-white/50">Modo</div>
                  <div className="text-cognitive-400 font-bold">Chat</div>
                </div>
                <div className="text-center p-3 rounded-xl bg-white/5">
                  <div className="text-sm text-white/50">Sesión</div>
                  <div className="text-white font-bold">#001</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="mt-8 text-center text-white/30 text-sm">
        Cognitive Server v0.1 • Sistema de Extracción Cognitiva con Prompts Vivos
      </footer>
    </div>
  );
}