    def _filter_think_chunk(self, chunk: str) -> str:
        """Filtrar etiquetas <think> de un chunk en tiempo real.
        
        Máquina de estados simplificada: Acumula en buffer hasta decidir si es texto o tag.
        """
        # Normalización Unicode
        chunk = chunk.replace('\\u003c', '<').replace('\\u003e', '>')
        chunk = chunk.replace('\u003c', '<').replace('\u003e', '>')
        
        self._think_filter_state["buffer"] += chunk
        buffer = self._think_filter_state["buffer"]
        
        if not self._think_filter_state["in_think_block"]:
            if '<think>' in buffer:
                # Detectado inicio: entregar lo anterior y entrar en modo oculto
                self._think_filter_state["in_think_block"] = True
                parts = buffer.split('<think>', 1)
                before = parts[0]
                # Mantener el resto para buscar el cierre
                self._think_filter_state["buffer"] = parts[1]
                # Recursión para procesar el resto del buffer inmediatamente
                return before + self._filter_think_chunk("")
            
            # Si hay un '<' sospechoso al final, esperar para no romper un posible tag
            last_angle = buffer.rfind('<')
            if last_angle != -1 and len(buffer) - last_angle < 8:
                # Retener la parte sospechosa en el buffer
                output = buffer[:last_angle]
                self._think_filter_state["buffer"] = buffer[last_angle:]
                return output
            
            # No hay tags: entregar todo y limpiar buffer
            self._think_filter_state["buffer"] = ""
            return buffer
        else:
            if '</think>' in buffer:
                # Detectado cierre: salir de modo oculto y procesar remanente
                self._think_filter_state["in_think_block"] = False
                parts = buffer.split('</think>', 1)
                after = parts[1]
                self._think_filter_state["buffer"] = ""
                # Recursión para procesar lo que venga después de </think>
                return self._filter_think_chunk(after)
            
            # Seguimos en modo oculto: limpiar buffer (consumir) y no entregar nada
            # Pero mantenemos el buffer si termina en '<' por si es parte de '</think>'
            last_angle = buffer.rfind('<')
            if last_angle != -1:
                # Mantener solo desde el último '<'
                self._think_filter_state["buffer"] = buffer[last_angle:]
            else:
                self._think_filter_state["buffer"] = ""
            return ""
