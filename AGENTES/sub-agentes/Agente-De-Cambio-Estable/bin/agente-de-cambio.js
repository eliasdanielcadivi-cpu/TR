#!/usr/bin/env node
/**
 * Agente de Cambio - CLI Standalone
 * 
 * Ejecuta el Agente de Cambio en modo standalone (sin ARES)
 * 
 * @example
 * ```bash
 * agente-de-cambio --help
 * agente-de-cambio --demo
 * agente-de-cambio --objective "Quiero lanzar mi producto en 3 meses"
 * ```
 */

import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { createInterface } from 'readline';
import { generateQuestion, parseAnswer, validateSchema } from './modules/questionnaire-engine/actions.ts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Colores para terminal
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

function printBanner() {
  console.log(`
${colors.cyan}╔═══════════════════════════════════════════════════════════╗
║     🧠 AGENTE DE CAMBIO - Sistema de Conducción Cognitiva    ║
║          Standalone CLI v0.1.0                                ║
╚═══════════════════════════════════════════════════════════╝${colors.reset}
  `);
}

function printHelp() {
  console.log(`
${colors.bright}USO:${colors.reset}
  agente-de-cambio [opciones]

${colors.bright}OPCIONES:${colors.reset}
  --help, -h              Mostrar esta ayuda
  --demo                  Ejecutar demostración con objetivo de ejemplo
  --objective, -o <texto> Declarar objetivo principal
  --domain, -d <dominio>  Dominio (cura, constructor, estudiante, emprendedor)
  --version, -v           Mostrar versión

${colors.bright}EJEMPLOS:${colors.reset}
  agente-de-cambio --demo
  agente-de-cambio -o "Quiero lanzar mi producto" -d emprendedor
  agente-de-cambio --objective "Quiero aprobar matemáticas" --domain estudiante

${colors.bright}RUTAS IMPORTANTES:${colors.reset}
  Directorio:     /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable
  Documentación:  /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/docs/CLAVE/
  Módulos:        /home/daniel/tron/programas/TR/AGENTES/sub-agentes/Agente-De-Cambio-Estable/modules/

${colors.bright}COMANDOS RELACIONADOS:${colors.reset}
  npm run dev                    Iniciar servidores (frontend + backend)
  npm run dev:server             Solo backend (puerto 3001)
  npm run dev:web                Solo frontend (puerto 3000)
  ares agente-de-cambio --prompt "..."  Invocar desde ARES
  `);
}

async function runDemo() {
  printBanner();
  
  console.log(`${colors.yellow}═══ DEMOSTRACIÓN - Objetivo: Lanzar producto ═══${colors.reset}\n`);
  
  // Objetivo de ejemplo
  const objective = {
    title: 'Lanzar producto SaaS',
    domain: 'emprendedor',
    deadline: '2026-06-19',
    metric: '100 usuarios pagando',
  };
  
  console.log(`${colors.blue}Objetivo:${colors.reset} ${objective.title}`);
  console.log(`${colors.blue}Dominio:${colors.reset} ${objective.domain}`);
  console.log(`${colors.blue}Deadline:${colors.reset} ${objective.deadline}`);
  console.log(`${colors.blue}Métrica:${colors.reset} ${objective.metric}\n`);
  
  // Simular flujo de preguntas
  const questions = [
    { field: 'has_prototype', context: { objective: 'launch_saas', domain: 'emprendedor' } },
    { field: 'current_stage', context: { objective: 'launch_saas', domain: 'emprendedor' } },
    { field: 'main_obstacle', context: { objective: 'launch_saas', domain: 'emprendedor' } },
  ];
  
  const answers = [];
  
  for (const q of questions) {
    const question = generateQuestion(q.field, q.context);
    
    console.log(`${colors.green}PREGUNTA:${colors.reset} ${question.prompt}`);
    console.log(`${colors.dim}Tipo: ${question.type}${colors.reset}\n`);
    
    if (question.options.length > 0) {
      console.log('Opciones:');
      question.options.forEach((opt, i) => {
        console.log(`  ${i + 1}. ${opt.label}`);
      });
    }
    
    console.log('');
  }
  
  console.log(`${colors.yellow}═══ FIN DEMOSTRACIÓN ═══${colors.reset}`);
  console.log(`\n${colors.dim}Para ejecutar con tu objetivo real:${colors.reset}`);
  console.log(`${colors.cyan}agente-de-cambio -o "Tu objetivo" -d tu_dominio${colors.reset}\n`);
}

async function interactiveMode(objective, domain) {
  printBanner();
  
  const rl = createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  
  const questionAsync = (query) => new Promise((resolve) => rl.question(query, resolve));
  
  try {
    console.log(`${colors.blue}Objetivo:${colors.reset} ${objective}`);
    console.log(`${colors.blue}Dominio:${colors.reset} ${domain}\n`);
    
    // Flujo interactivo
    const context = { objective: 'user_objective', domain };
    const fields = ['has_prototype', 'current_stage', 'has_team', 'main_obstacle'];
    const answers = [];
    
    for (const field of fields) {
      const question = generateQuestion(field, context);
      
      console.log(`\n${colors.green}${question.prompt}${colors.reset}`);
      
      if (question.options.length > 0) {
        question.options.forEach((opt, i) => {
          console.log(`  ${colors.cyan}${i + 1}.${colors.reset} ${opt.label}`);
        });
        console.log(`  ${colors.dim}O escribe tu respuesta...${colors.reset}`);
      }
      
      const answer = await questionAsync('> ');
      
      const parsed = parseAnswer(question, {
        selected: answer,
        text: answer,
      });
      
      answers.push(parsed);
      console.log(`${colors.dim}✓ Respuesta registrada${colors.reset}`);
    }
    
    // Validar schema
    const requiredFields = ['has_prototype', 'current_stage'];
    const isValid = validateSchema(answers, requiredFields);
    
    console.log(`\n${colors.blue}═══ RESUMEN ═══${colors.reset}`);
    console.log(`Campos completados: ${answers.length}`);
    console.log(`Schema válido: ${isValid ? colors.green + 'Sí' + colors.reset : colors.red + 'No' + colors.reset}`);
    
  } finally {
    rl.close();
  }
}

// Main
async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    printHelp();
    return;
  }
  
  if (args.includes('--version') || args.includes('-v')) {
    console.log('Agente de Cambio CLI v0.1.0');
    return;
  }
  
  if (args.includes('--demo')) {
    await runDemo();
    return;
  }
  
  const objectiveIndex = args.indexOf('--objective') !== -1 ? args.indexOf('--objective') : args.indexOf('-o');
  const domainIndex = args.indexOf('--domain') !== -1 ? args.indexOf('--domain') : args.indexOf('-d');
  
  if (objectiveIndex !== -1 && args[objectiveIndex + 1]) {
    const objective = args[objectiveIndex + 1];
    const domain = domainIndex !== -1 && args[domainIndex + 1] ? args[domainIndex + 1] : 'emprendedor';
    
    await interactiveMode(objective, domain);
    return;
  }
  
  // Sin argumentos → mostrar help
  printHelp();
}

main().catch(console.error);
