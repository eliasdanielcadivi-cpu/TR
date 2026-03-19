import axios, { AxiosInstance } from 'axios';

export interface DeepSeekMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface DeepSeekCompletionRequest {
  messages: DeepSeekMessage[];
  model?: string;
  temperature?: number;
  stream?: boolean;
  max_tokens?: number;
  response_format?: { type: 'json_object' | 'text' };
}

export interface DeepSeekCompletionResponse {
  id: string;
  choices: Array<{
    message: DeepSeekMessage;
    finish_reason: string;
    index: number;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
    prompt_cache_hit_tokens?: number;
    prompt_cache_miss_tokens?: number;
  };
}

export interface DeepSeekStreamChunk {
  id: string;
  choices: Array<{
    delta: {
      content?: string;
      role?: string;
    };
    finish_reason: string | null;
    index: number;
  }>;
  created: number;
  model: string;
}

export class DeepSeekClient {
  private client: AxiosInstance;
  private apiKey: string;
  private baseURL = 'https://api.deepseek.com';

  constructor(apiKey: string) {
    this.apiKey = apiKey;
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
    });
  }

  async createCompletion(
    request: DeepSeekCompletionRequest
  ): Promise<DeepSeekCompletionResponse> {
    const payload = {
      model: request.model || 'deepseek-chat',
      messages: request.messages,
      temperature: request.temperature || 0.7,
      stream: false,
      max_tokens: request.max_tokens || 4096,
      response_format: request.response_format,
    };

    const response = await this.client.post<DeepSeekCompletionResponse>(
      '/chat/completions',
      payload
    );
    return response.data;
  }

  async *createCompletionStream(
    request: DeepSeekCompletionRequest
  ): AsyncGenerator<DeepSeekStreamChunk> {
    const payload = {
      model: request.model || 'deepseek-chat',
      messages: request.messages,
      temperature: request.temperature || 0.7,
      stream: true,
      max_tokens: request.max_tokens || 4096,
      response_format: request.response_format,
    };

    const response = await this.client.post(
      '/chat/completions',
      payload,
      {
        responseType: 'stream',
        headers: {
          'Accept': 'text/event-stream',
        },
      }
    );

    const stream = response.data;
    const decoder = new TextDecoder();
    let buffer = '';

    for await (const chunk of stream) {
      buffer += decoder.decode(chunk, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') return;

          try {
            const parsed: DeepSeekStreamChunk = JSON.parse(data);
            yield parsed;
          } catch (error) {
            console.error('Error parsing SSE chunk:', error);
          }
        }
      }
    }
  }
}