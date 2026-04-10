// results.js
// Запрашивает /api/results, рисует карту и таблицы

async function fetchData() {
    const res = await fetch('/api/results');
    if (!res.ok) {
      console.error('Failed to fetch /api/results');
      return null;
    }
    return await res.json();
  }
  
  function formatDateTime(s) {
    try {
      const d = new Date(s);
      if (!isNaN(d)) {
        return d.toLocaleString();
      }
    } catch(e){}
    return s;
  }

  function formatTime(s) {
    try {
      const d = new Date(s);
      if (!isNaN(d)) {
        return d.toLocaleTimeString();
      }
    } catch(e){}
    return s;
  }

  // Функция для отображения логов планирования
  function renderPlanningLogs(logs) {
    const logContainer = document.getElementById('planning-log');
    
    if (!logs || logs.length === 0) {
      logContainer.innerHTML = '<div class="log-placeholder">Запустите планирование для просмотра процесса...</div>';
      return;
    }

    let html = '';
    logs.forEach(log => {
      const timestamp = new Date(log.timestamp).toLocaleTimeString();
      const logClass = `log-entry log-${log.type}`;
      
      html += `
        <div class="${logClass}">
          <span class="log-time">[${timestamp}]</span>
          <span class="log-message">${log.message}</span>
        </div>
      `;
    });

    logContainer.innerHTML = html;
    
    // Автопрокрутка вниз если включена
    if (document.getElementById('auto-scroll').classList.contains('active')) {
      logContainer.scrollTop = logContainer.scrollHeight;
    }
  }
  
  function build() {
    fetchData().then(data => {
      if (!data) return;
      const baseX = data.base_x;
      const baseY = data.base_y;

      document.getElementById('hub-coords').innerText = `${baseX.toFixed(6)}, ${baseY.toFixed(6)}`;

      // Stats
      document.getElementById('stat-drones').innerText = data.drones.length;
      document.getElementById('stat-orders').innerText = data.orders.length;
      document.getElementById('stat-ops').innerText = data.operations.length;

      // Рендерим логи планирования
      renderPlanningLogs(data.planning_logs);

      // Build map
      const map = L.map('map').setView([baseX, baseY], 12);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap, © CartoDB'
      }).addTo(map);

      // Hub marker
      const hubIcon = L.circleMarker([baseX, baseY], {radius:8, color:'#0b84ff', fillColor:'#0b84ff', fillOpacity:1}).addTo(map).bindPopup('Хаб');

      // Orders
      const orderIcon = L.icon({
        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        iconSize: [25,41],
        iconAnchor: [12,41]
      });

      const ordersMap = {};
      data.orders.forEach(o => {
        const marker = L.marker([o.X, o.Y], {icon: orderIcon})
          .addTo(map)
          .bindPopup(`Заказ ${o.ID}<br>Вес: ${o.Weight} кг<br>Стоимость: ${o.Cost}`);
        ordersMap[o.ID] = marker;
      });

      // Routes by drone
      const opsByDrone = {};
      data.operations.forEach(op => {
        if (!opsByDrone[op.DroneID]) opsByDrone[op.DroneID] = [];
        opsByDrone[op.DroneID].push(op);
      });

      const colors = ['#16a34a','#ef4444','#f59e0b','#0ea5e9','#7c3aed','#e11d48','#0f172a'];
      let colorIdx = 0;

      // Table ops
      const opsTBody = document.querySelector('#ops-table tbody');
      opsTBody.innerHTML = '';
      data.operations.forEach(op => {
        const tr = document.createElement('tr');
        const ordersStr = op.OrderIDs && op.OrderIDs.length ? op.OrderIDs.join(';') : '';
        tr.innerHTML = `<td>${op.ID}</td>
                        <td>${op.OperationType}</td>
                        <td>${op.DroneID}</td>
                        <td>${formatDateTime(op.PlanTimeStart)}</td>
                        <td>${formatDateTime(op.PlanTimeEnd)}</td>
                        <td>${ordersStr}</td>
                        <td>${op.XStart.toFixed(6)}, ${op.YStart.toFixed(6)} → ${op.XEnd.toFixed(6)}, ${op.YEnd.toFixed(6)}</td>
                        <td>${op.SumCapacity}</td>`;
        opsTBody.appendChild(tr);
      });

      // Информация по дронам - ИСПРАВЛЕННАЯ ФУНКЦИЯ
      const dronesInfo = document.getElementById('drones-info');
      dronesInfo.innerHTML = '';

      // Создаем информацию для каждого дрона
      data.drones.forEach(drone => {
        const droneOps = opsByDrone[drone.ID] || [];
        const sortedOps = droneOps.sort((a,b) => new Date(a.PlanTimeStart) - new Date(b.PlanTimeStart));
        
        // Собираем все заказы этого дрона
        const droneOrders = [];
        sortedOps.forEach(op => {
          if (op.OrderIDs && op.OrderIDs.length > 0) {
            op.OrderIDs.forEach(orderID => {
              const order = data.orders.find(o => o.ID == orderID);
              if (order && !droneOrders.find(o => o.ID == orderID)) {
                droneOrders.push(order);
              }
            });
          }
        });

        // Рассчитываем статистику
        const totalOrders = droneOrders.length;
        const totalWeight = droneOrders.reduce((sum, order) => sum + order.Weight, 0);
        const totalCost = droneOrders.reduce((sum, order) => sum + order.Cost, 0);
        const firstOp = sortedOps[0];
        const lastOp = sortedOps[sortedOps.length - 1];
        const workTime = firstOp && lastOp ? 
          Math.round((new Date(lastOp.PlanTimeEnd) - new Date(firstOp.PlanTimeStart)) / (1000 * 60)) : 0;

        // Создаем блок информации о дроне
        const droneBlock = document.createElement('div');
        droneBlock.className = 'drone-block';
        droneBlock.innerHTML = `
          <div class="drone-header">
            <h3>${drone.Label} (ID: ${drone.ID})</h3>
            <span class="drone-color" style="background-color: ${colors[colorIdx % colors.length]}"></span>
          </div>
          <div class="drone-stats">
            <div class="stat-row">
              <span class="stat-label">Грузоподъемность:</span>
              <span class="stat-value">${drone.MaxCapacity} кг</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Скорость:</span>
              <span class="stat-value">${drone.Speed} км/ч</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Батарея:</span>
              <span class="stat-value">${drone.BatteryLife} мин</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Заказов выполнено:</span>
              <span class="stat-value">${totalOrders} шт</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Общий вес доставлен:</span>
              <span class="stat-value">${totalWeight.toFixed(1)} кг</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Общий доход:</span>
              <span class="stat-value">${totalCost.toFixed(0)} руб</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Время работы:</span>
              <span class="stat-value">${workTime} мин</span>
            </div>
          </div>
          ${droneOrders.length > 0 ? `
            <div class="drone-orders">
              <strong>Заказы дрона:</strong>
              <div class="orders-list">
                ${droneOrders.map(order => 
                  `<div class="order-item">№${order.ID} - ${order.Weight}кг - ${order.Cost}руб</div>`
                ).join('')}
              </div>
            </div>
          ` : '<div class="no-orders">Нет выполненных заказов</div>'}
          <div class="drone-schedule">
            <strong>Расписание:</strong>
            <div class="schedule-item">Начало: ${firstOp ? formatTime(firstOp.PlanTimeStart) : '—'}</div>
            <div class="schedule-item">Окончание: ${lastOp ? formatTime(lastOp.PlanTimeEnd) : '—'}</div>
          </div>
        `;

        dronesInfo.appendChild(droneBlock);

        // Рисуем маршрут на карте (если есть операции)
        if (sortedOps.length > 0) {
          const latlngs = [];
          sortedOps.forEach(op => {
            latlngs.push([op.XStart, op.YStart]);
            latlngs.push([op.XEnd, op.YEnd]);
          });

          const seq = [];
          for (let i=0;i<latlngs.length;i++){
            const cur = latlngs[i];
            if (seq.length===0 || seq[seq.length-1][0] !== cur[0] || seq[seq.length-1][1] !== cur[1]) {
              seq.push(cur);
            }
          }

          const color = colors[(colorIdx) % colors.length];
          const poly = L.polyline(seq, {color: color, weight: 4, opacity:0.85}).addTo(map);
          
          // Добавляем информацию о дроне в popup
          const popupContent = `
            <div class="map-popup">
              <h4>${drone.Label}</h4>
              <p>Заказов: ${totalOrders}</p>
              <p>Вес: ${totalWeight.toFixed(1)} кг</p>
              <p>Доход: ${totalCost.toFixed(0)} руб</p>
              <p>Время работы: ${workTime} мин</p>
            </div>
          `;
          poly.bindPopup(popupContent);

          // Точки маршрута
          seq.forEach((p, idx) => {
            L.circleMarker(p, {radius:4, color: color}).addTo(map);
          });
        }

        colorIdx++;
      });

    }).catch(err => {
      console.error(err);
    });
  }
  
  // Обработчики для кнопок управления логами
  document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('refresh').addEventListener('click', build);
    
    const clearLogBtn = document.getElementById('clear-log');
    if (clearLogBtn) {
      clearLogBtn.addEventListener('click', function() {
        document.getElementById('planning-log').innerHTML = 
          '<div class="log-placeholder">Логи очищены</div>';
      });
    }

    const autoScrollBtn = document.getElementById('auto-scroll');
    if (autoScrollBtn) {
      autoScrollBtn.addEventListener('click', function() {
        this.classList.toggle('active');
      });
    }
  });

  setInterval(build, 5000);
  window.addEventListener('load', build);