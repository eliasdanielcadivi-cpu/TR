'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { io, Socket } from 'socket.io-client';
import { useChatStore } from '@/app/store/chatStore';
import type {
  ClientToServerEvents,
  ServerToClientEvents,
} from '@/types/socket';

interface SocketContextType {
  socket: Socket<ServerToClientEvents, ClientToServerEvents> | null;
  isConnected: boolean;
  sendMessage: (content: string) => void;
  updatePrompt: (content: string) => void;
}

const SocketContext = createContext<SocketContextType>({
  socket: null,
  isConnected: false,
  sendMessage: () => {},
  updatePrompt: () => {},
});

const SOCKET_URL = process.env.NEXT_PUBLIC_SOCKET_URL || 'http://localhost:3001';

export function SocketProvider({ children }: { children: ReactNode }) {
  const [socket, setSocket] = useState<Socket<ServerToClientEvents, ClientToServerEvents> | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  const {
    sessionId,
    setSessionId,
    addMessage,
    setCurrentQuestion,
    setMode,
    addPromptMutation,
    setDeltaMetrics,
    setIsStreaming,
    mode,
    isReasoning,
  } = useChatStore();

  useEffect(() => {
    const socketInstance = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    setSocket(socketInstance);

    // Connection events
    socketInstance.on('connect', () => {
      console.log('Socket connected:', socketInstance.id);
      setIsConnected(true);

      // Initialize or restore session
      socketInstance.emit('session:init', sessionId);
    });

    socketInstance.on('disconnect', () => {
      console.log('Socket disconnected');
      setIsConnected(false);
    });

    // Message streaming
    socketInstance.on('message:stream', (chunk: string) => {
      // Handle streaming chunks
      // We'll update the last message with streaming content
      setIsStreaming(true);
      console.log('Stream chunk:', chunk);
      // TODO: Implement streaming UI update
    });

    socketInstance.on('message:complete', (message) => {
      setIsStreaming(false);
      addMessage({
        ...message,
        timestamp: new Date(message.timestamp),
      });
    });

    socketInstance.on('prompt:mutation', (mutation) => {
      addPromptMutation({
        ...mutation,
        timestamp: new Date(mutation.timestamp),
      });
    });

    socketInstance.on('question:next', (question) => {
      setCurrentQuestion(question);
    });

    socketInstance.on('mode:switch', (mode) => {
      setMode(mode);
    });

    socketInstance.on('delta:update', (delta) => {
      setDeltaMetrics(delta);
    });

    socketInstance.on('error', (error) => {
      console.error('Socket error:', error);
    });

    return () => {
      socketInstance.disconnect();
    };
  }, [sessionId]);

  const sendMessage = (content: string) => {
    if (!socket || !isConnected) {
      console.error('Socket not connected');
      return;
    }

    const context = {
      isReasoning,
      sessionId: sessionId || '',
    };

    socket.emit('message:send', content, mode, context);
  };

  const updatePrompt = (content: string) => {
    if (!socket || !isConnected) return;
    socket.emit('prompt:update', content);
  };

  return (
    <SocketContext.Provider value={{ socket, isConnected, sendMessage, updatePrompt }}>
      {children}
    </SocketContext.Provider>
  );
}

export const useSocket = () => useContext(SocketContext);