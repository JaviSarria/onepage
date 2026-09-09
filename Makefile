# OnePage — Makefile de mantenimiento
# Objetivos: build, start (start_be/start_fe), stop (stop_be/stop_fe)

BE_DIR := onepage-be
FE_DIR := onepage-fe
RUN_DIR := .run
BE_PORT ?= 8000
FE_PORT ?= 5173

.PHONY: help build build_be build_fe start start_be start_fe stop stop_be stop_fe restart status clean

help:
	@echo OnePage - objetivos disponibles:
	@echo   build      Instala dependencias de backend y frontend y compila el frontend
	@echo   start      Arranca backend y frontend
	@echo   start_be   Arranca solo el backend (FastAPI, puerto $(BE_PORT))
	@echo   start_fe   Arranca solo el frontend (Vite, puerto $(FE_PORT))
	@echo   stop       Detiene backend y frontend
	@echo   stop_be    Detiene solo el backend
	@echo   stop_fe    Detiene solo el frontend
	@echo   restart    stop + start
	@echo   status     Muestra el estado de los procesos
	@echo   clean      Elimina artefactos de compilacion y ficheros de PID

ifeq ($(OS),Windows_NT)

PS := powershell -NoProfile -ExecutionPolicy Bypass -Command

build_be:
	@$(PS) "Push-Location '$(BE_DIR)'; uv sync; Pop-Location"

build_fe:
	@$(PS) "Push-Location '$(FE_DIR)'; npm install; npm run build; Pop-Location"

start_be:
	@$(PS) "New-Item -ItemType Directory -Force '$(RUN_DIR)' | Out-Null; $$p = Start-Process -PassThru -WindowStyle Hidden -FilePath 'uv' -ArgumentList @('run','--directory','$(BE_DIR)','python','-m','uvicorn','onepage_be.main:app','--host','127.0.0.1','--port','$(BE_PORT)'); $$p.Id | Out-File -Encoding ascii '$(RUN_DIR)/be.pid'; Write-Host ('backend iniciado en http://127.0.0.1:$(BE_PORT) (PID ' + $$p.Id + ')')"

start_fe:
	@$(PS) "New-Item -ItemType Directory -Force '$(RUN_DIR)' | Out-Null; $$p = Start-Process -PassThru -WindowStyle Hidden -FilePath 'npm.cmd' -ArgumentList @('run','dev') -WorkingDirectory '$(FE_DIR)'; $$p.Id | Out-File -Encoding ascii '$(RUN_DIR)/fe.pid'; Write-Host ('frontend iniciado en http://127.0.0.1:$(FE_PORT) (PID ' + $$p.Id + ')')"

stop_be:
	@$(PS) "$$f='$(RUN_DIR)/be.pid'; if (Test-Path $$f) { $$id=(Get-Content $$f -Raw).Trim(); taskkill /PID $$id /T /F 2>&1 | Out-Null; Remove-Item $$f -Force }; $$owners=Get-NetTCPConnection -State Listen -LocalPort $(BE_PORT) -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; foreach ($$owner in $$owners) { taskkill /PID $$owner /T /F 2>&1 | Out-Null }; Write-Host 'backend detenido'"

stop_fe:
	@$(PS) "$$f='$(RUN_DIR)/fe.pid'; if (Test-Path $$f) { $$id=(Get-Content $$f -Raw).Trim(); taskkill /PID $$id /T /F 2>&1 | Out-Null; Remove-Item $$f -Force }; $$owners=Get-NetTCPConnection -State Listen -LocalPort $(FE_PORT) -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique; foreach ($$owner in $$owners) { taskkill /PID $$owner /T /F 2>&1 | Out-Null }; Write-Host 'frontend detenido'"

status:
	@$(PS) "Get-ChildItem '$(RUN_DIR)/*.pid' -ErrorAction SilentlyContinue | ForEach-Object { $$id=[int]((Get-Content $$_ -Raw).Trim()); $$activo=[bool](Get-Process -Id $$id -ErrorAction SilentlyContinue); Write-Host ($$_.BaseName + ': ' + $$(if ($$activo) { 'activo (PID ' + $$id + ')' } else { 'parado' })) }"

clean:
	@$(PS) "Remove-Item -Recurse -Force '$(FE_DIR)/dist','$(RUN_DIR)' -ErrorAction SilentlyContinue; Write-Host 'limpieza completada'"

else

build_be:
	cd $(BE_DIR) && uv sync

build_fe:
	cd $(FE_DIR) && npm install && npm run build

start_be:
	@mkdir -p $(RUN_DIR)
	@uv run --directory $(BE_DIR) python -m uvicorn onepage_be.main:app --host 127.0.0.1 --port $(BE_PORT) > $(RUN_DIR)/be.log 2>&1 & echo $$! > $(RUN_DIR)/be.pid
	@echo "backend iniciado en http://127.0.0.1:$(BE_PORT)"

start_fe:
	@mkdir -p $(RUN_DIR)
	@npm run --prefix $(FE_DIR) dev > $(RUN_DIR)/fe.log 2>&1 & echo $$! > $(RUN_DIR)/fe.pid
	@echo "frontend iniciado en http://127.0.0.1:$(FE_PORT)"

stop_be:
	@if [ -f $(RUN_DIR)/be.pid ]; then kill $$(cat $(RUN_DIR)/be.pid) 2>/dev/null; rm -f $(RUN_DIR)/be.pid; echo "backend detenido"; else echo "backend no estaba en ejecucion"; fi

stop_fe:
	@if [ -f $(RUN_DIR)/fe.pid ]; then kill $$(cat $(RUN_DIR)/fe.pid) 2>/dev/null; rm -f $(RUN_DIR)/fe.pid; echo "frontend detenido"; else echo "frontend no estaba en ejecucion"; fi

status:
	@for f in $(RUN_DIR)/*.pid; do [ -e "$$f" ] || continue; if kill -0 $$(cat $$f) 2>/dev/null; then echo "$$(basename $$f .pid): activo"; else echo "$$(basename $$f .pid): parado"; fi; done

clean:
	rm -rf $(FE_DIR)/dist $(RUN_DIR)

endif

build: build_be build_fe

start: start_be start_fe

stop: stop_fe stop_be

restart: stop start
