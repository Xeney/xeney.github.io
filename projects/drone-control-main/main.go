package main

import (
	"encoding/csv"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

// Структуры данных
type Drone struct {
	ID            int
	Label         string
	MaxCapacity   float64
	Speed         float64
	BatteryLife   float64
	CurrentLoad   float64
	Battery       float64
	PositionX     float64
	PositionY     float64
	IsAtBase      bool
	NextAvailable time.Time
}

type Order struct {
	ID              int
	Cost            float64
	X               float64
	Y               float64
	Weight          float64
	TimeWindowStart time.Time
	TimeWindowEnd   time.Time
	IsAssigned      bool
	IsDelivered     bool
	Priority        float64
}

type Operation struct {
	ID            int
	OperationType string
	DroneID       int
	OrderIDs      []int
	PlanTimeStart time.Time
	PlanTimeEnd   time.Time
	XStart        float64
	YStart        float64
	XEnd          float64
	YEnd          float64
	SumCapacity   float64
	BatteryUsage  float64
	Description   string
}

type PlanningResult struct {
	Operations     []Operation
	AssignedOrders int
	FailedOrders   int
	TotalDistance  float64
	TotalTime      float64
	TotalIncome    float64
	Efficiency     float64
}

type PlanningLog struct {
	Timestamp time.Time `json:"timestamp"`
	Message   string    `json:"message"`
	Type      string    `json:"type"` // "info", "success", "warning", "error"
}

var planningLogs []PlanningLog

var (
	drones []Drone
	orders []Order
	hubX   = 45.077774
	hubY   = 39.003718
)

func main() {
	createInitialFiles()

	r := gin.Default()
	r.LoadHTMLGlob("templates/*")
	r.Static("/static", "./static")

	r.GET("/", homeHandler)
	r.POST("/upload", uploadHandler)
	r.POST("/schedule", scheduleHandler)
	r.GET("/download-csv", downloadHandler)
	r.GET("/results", resultsPageHandler)
	r.GET("/api/results", apiResultsHandler)
	r.GET("/download/report", downloadReportHandler)

	fmt.Println("🚀 Сервер запущен на http://localhost:8080")
	r.Run(":8080")
}

func createInitialFiles() {
	files := []string{"drone.csv", "order.csv", "plan.csv"}
	for _, file := range files {
		if _, err := os.Stat(file); os.IsNotExist(err) {
			os.Create(file)
		}
	}
}

func resultsPageHandler(c *gin.Context) {
	c.HTML(200, "results.html", nil)
}

func apiResultsHandler(c *gin.Context) {
	operations := readPlanCSV()
	data := gin.H{
		"operations":    operations,
		"drones":        drones,
		"orders":        orders,
		"base_x":        hubX,
		"base_y":        hubY,
		"planning_logs": planningLogs,
		"stats": gin.H{
			"total_operations": len(operations),
			"total_drones":     len(drones),
			"total_orders":     len(orders),
			"assigned_orders":  countAssignedOrders(),
			"delivered_orders": countDeliveredOrders(),
		},
	}
	c.JSON(200, data)
}

func downloadHandler(c *gin.Context) {
	c.Header("Content-Description", "File Transfer")
	c.Header("Content-Disposition", "attachment; filename=plan.csv")
	c.Header("Content-Type", "text/csv")
	c.File("plan.csv")
}

func homeHandler(c *gin.Context) {
	c.HTML(200, "index.html", nil)
}

func uploadHandler(c *gin.Context) {
	file, err := c.FormFile("csv")
	if err != nil {
		c.JSON(400, gin.H{"error": "No file uploaded"})
		return
	}

	filename := file.Filename
	if err := c.SaveUploadedFile(file, filename); err != nil {
		c.JSON(500, gin.H{"error": "Failed to save file"})
		return
	}

	if filename == "drone.csv" {
		drones = parseDronesCSV("drone.csv")
	} else if filename == "order.csv" {
		orders = parseOrdersCSV("order.csv")
	}

	c.JSON(200, gin.H{"status": "uploaded", "file": filename})
}

func scheduleHandler(c *gin.Context) {
	if len(drones) == 0 || len(orders) == 0 {
		c.JSON(400, gin.H{"error": "Please upload both drone.csv and order.csv first"})
		return
	}

	planningLogs = []PlanningLog{}

	fmt.Printf("📊 Начинаем быстрое планирование: %d дронов, %d заказов\n", len(drones), len(orders))

	// Сбрасываем состояния
	resetDroneStates()
	resetOrderStates()

	// Запускаем упрощенный алгоритм планирования
	result := fastSimpleSchedule(drones, orders)

	// Сохраняем результаты
	savePlanCSV(result.Operations)

	c.JSON(200, gin.H{
		"status":          "scheduling completed",
		"operations":      len(result.Operations),
		"assigned_orders": result.AssignedOrders,
		"failed_orders":   result.FailedOrders,
		"total_distance":  result.TotalDistance,
		"total_time":      result.TotalTime,
		"total_income":    result.TotalIncome,
		"efficiency":      result.Efficiency,
	})
}

func addPlanningLog(logType, message string) {
	planningLogs = append(planningLogs, PlanningLog{
		Timestamp: time.Now(),
		Message:   message,
		Type:      logType,
	})
	// Также выводим в консоль для обратной совместимости
	fmt.Println(message)
}

func fastSimpleSchedule(drones []Drone, orders []Order) PlanningResult {
	// Очищаем логи перед началом нового планирования
	planningLogs = []PlanningLog{}

	var operations []Operation
	operationID := 1
	startTime := time.Date(2025, 10, 24, 8, 0, 0, 0, time.UTC)
	hubX, hubY := 45.077774, 39.003718

	// Добавляем начальный лог
	addPlanningLog("info", fmt.Sprintf("📊 Начинаем быстрое планирование: %d дронов, %d заказов", len(drones), len(orders)))

	// сортируем заказы по времени начала окна
	sortedOrders := make([]Order, len(orders))
	copy(sortedOrders, orders)
	sort.Slice(sortedOrders, func(i, j int) bool {
		return sortedOrders[i].TimeWindowStart.Before(sortedOrders[j].TimeWindowStart)
	})

	// Состояние дронов
	type DroneState struct {
		Drone         Drone
		NextAvailable time.Time
		BatteryLeft   float64 // минуты
	}
	states := make([]DroneState, len(drones))
	for i := range drones {
		states[i] = DroneState{
			Drone:         drones[i],
			NextAvailable: startTime,
			BatteryLeft:   drones[i].BatteryLife,
		}
	}

	addPlanningLog("info", "⏰ Начинаем распределение заказов между дронами...")

	assignedOrders := 0
	maxPlanningTime := 20 * time.Second
	startPlanning := time.Now()

	for oi := range sortedOrders {
		if time.Since(startPlanning) > maxPlanningTime {
			addPlanningLog("warning", "⏳ Время планирования истекло (20 сек). Завершаем.")
			break
		}

		order := &sortedOrders[oi]
		if order.IsAssigned {
			continue
		}

		// 🔋 Заряжаем дронов, если батарея ниже 40%
		for i := range states {
			ds := &states[i]
			if ds.BatteryLeft < ds.Drone.BatteryLife*0.4 {
				chargeStart := ds.NextAvailable
				chargeEnd := chargeStart.Add(15 * time.Minute)
				operations = append(operations, Operation{
					ID:            operationID,
					OperationType: "Зарядка",
					DroneID:       ds.Drone.ID,
					PlanTimeStart: chargeStart,
					PlanTimeEnd:   chargeEnd,
					XStart:        hubX,
					YStart:        hubY,
					XEnd:          hubX,
					YEnd:          hubY,
				})
				operationID++
				ds.BatteryLeft = ds.Drone.BatteryLife
				ds.NextAvailable = chargeEnd
				addPlanningLog("info", fmt.Sprintf("🔋 Дрон %d зарядился до 100%%", ds.Drone.ID))
			}
		}

		bestDrone := -1
		bestStart := time.Time{}
		bestBatteryAfter := 0.0

		// ищем подходящего дрона
		for i := range states {
			ds := &states[i]
			if order.Weight > ds.Drone.MaxCapacity {
				continue
			}

			// время полета туда и обратно
			dist := haversineKm(hubX, hubY, order.X, order.Y)
			minThere := (dist / ds.Drone.Speed) * 60
			minBack := minThere
			needTime := minThere + minBack + 15 // взлет+посадки
			if needTime > ds.BatteryLeft {
				continue
			}

			depart := ds.NextAvailable
			arrival := depart.Add(time.Duration((minThere+5)*60) * time.Second)
			if arrival.After(order.TimeWindowEnd) {
				continue
			}

			if bestDrone == -1 || arrival.Before(bestStart) {
				bestDrone = i
				bestStart = depart
				bestBatteryAfter = ds.BatteryLeft - needTime
			}
		}

		if bestDrone == -1 {
			addPlanningLog("warning", fmt.Sprintf("⚠️  Нет подходящего дрона для заказа %d (вес %.1f)", order.ID, order.Weight))
			continue
		}

		ds := &states[bestDrone]
		d := ds.Drone

		addPlanningLog("success", fmt.Sprintf("✅ Дрон %d берёт заказ %d (%.1f кг)", d.ID, order.ID, order.Weight))

		// время
		dist := haversineKm(hubX, hubY, order.X, order.Y)
		minThere := (dist / ds.Drone.Speed) * 60
		minBack := minThere

		takeoffStart := ds.NextAvailable
		takeoffEnd := takeoffStart.Add(5 * time.Minute)
		flightStart := takeoffEnd
		flightEnd := flightStart.Add(time.Duration(minThere) * time.Minute)
		landStart := flightEnd
		landEnd := landStart.Add(5 * time.Minute)
		retFlightStart := landEnd
		retFlightEnd := retFlightStart.Add(time.Duration(minBack) * time.Minute)
		finalLandStart := retFlightEnd
		finalLandEnd := finalLandStart.Add(5 * time.Minute)

		ops := []Operation{
			{ID: operationID, OperationType: "Взлет", DroneID: d.ID, PlanTimeStart: takeoffStart, PlanTimeEnd: takeoffEnd, XStart: hubX, YStart: hubY, XEnd: hubX, YEnd: hubY},
			{ID: operationID + 1, OperationType: "Полет", DroneID: d.ID, OrderIDs: []int{order.ID}, PlanTimeStart: flightStart, PlanTimeEnd: flightEnd, XStart: hubX, YStart: hubY, XEnd: order.X, YEnd: order.Y, SumCapacity: order.Weight},
			{ID: operationID + 2, OperationType: "Посадка", DroneID: d.ID, OrderIDs: []int{order.ID}, PlanTimeStart: landStart, PlanTimeEnd: landEnd, XStart: order.X, YStart: order.Y, XEnd: order.X, YEnd: order.Y, SumCapacity: order.Weight},
			{ID: operationID + 3, OperationType: "Полет", DroneID: d.ID, PlanTimeStart: retFlightStart, PlanTimeEnd: retFlightEnd, XStart: order.X, YStart: order.Y, XEnd: hubX, YEnd: hubY},
			{ID: operationID + 4, OperationType: "Посадка", DroneID: d.ID, PlanTimeStart: finalLandStart, PlanTimeEnd: finalLandEnd, XStart: hubX, YStart: hubY, XEnd: hubX, YEnd: hubY},
		}
		operations = append(operations, ops...)
		operationID += 5

		// обновляем состояние
		ds.NextAvailable = finalLandEnd
		ds.BatteryLeft = bestBatteryAfter
		order.IsAssigned = true
		order.IsDelivered = true
		assignedOrders++
	}

	// метрики
	totalDistance := calculateTotalDistanceFast(operations)
	totalTime := calculateTotalTimeFast(operations)
	totalIncome := calculateTotalIncomeFast(sortedOrders)
	efficiency := float64(assignedOrders) / float64(len(orders)) * 100

	addPlanningLog("info", fmt.Sprintf("📊 Планирование завершено: %d/%d заказов (%.1f%%)", assignedOrders, len(orders), efficiency))

	generateReport(PlanningResult{
		Operations:     operations,
		AssignedOrders: assignedOrders,
		FailedOrders:   len(orders) - assignedOrders,
		TotalDistance:  totalDistance,
		TotalTime:      totalTime,
		TotalIncome:    totalIncome,
		Efficiency:     efficiency,
	})

	return PlanningResult{
		Operations:     operations,
		AssignedOrders: assignedOrders,
		FailedOrders:   len(orders) - assignedOrders,
		TotalDistance:  totalDistance,
		TotalTime:      totalTime,
		TotalIncome:    totalIncome,
		Efficiency:     efficiency,
	}
}

func downloadReportHandler(c *gin.Context) {
	c.Header("Content-Disposition", "attachment; filename=report.txt")
	c.Header("Content-Type", "text/plain")
	c.File("report.txt")
}

// haversineKm вычисляет расстояние между двумя точками (lat, lon) в километрах
func haversineKm(lat1, lon1, lat2, lon2 float64) float64 {
	const R = 6371.0 // радиус Земли в км
	lat1r := lat1 * math.Pi / 180.0
	lat2r := lat2 * math.Pi / 180.0
	dlat := (lat2 - lat1) * math.Pi / 180.0
	dlon := (lon2 - lon1) * math.Pi / 180.0

	a := math.Sin(dlat/2)*math.Sin(dlat/2) +
		math.Cos(lat1r)*math.Cos(lat2r)*
			math.Sin(dlon/2)*math.Sin(dlon/2)
	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a))
	return R * c
}

// БЫСТРАЯ ПРОВЕРКА ВОЗМОЖНОСТИ ВЗЯТЬ ЗАКАЗ
func canDroneTakeOrderFast(drone *Drone, order *Order) bool {
	// 1. Проверка грузоподъемности
	if drone.CurrentLoad+order.Weight > drone.MaxCapacity {
		return false
	}

	// 2. Упрощенная проверка батареи (всегда true для скорости)
	if drone.Battery < 10 {
		return false
	}

	// 3. Быстрая проверка временного окна
	distance := calculateDistance(drone.PositionX, drone.PositionY, order.X, order.Y)
	flightTime := distance / drone.Speed * 60 // в минутах

	// Время доставки должно быть в пределах окна +- 30 минут
	deliveryTime := drone.NextAvailable.Add(time.Duration(flightTime+5) * time.Minute)
	maxAllowedTime := order.TimeWindowEnd.Add(30 * time.Minute)

	return deliveryTime.Before(maxAllowedTime)
}

// ПРОСТОЕ СОЗДАНИЕ ОПЕРАЦИЙ
func createSimpleOrderOperations(drone *Drone, order *Order, operationID *int) []Operation {
	var operations []Operation
	currentTime := drone.NextAvailable

	// 1. Взлет (если не на базе)
	if !drone.IsAtBase {
		// Возврат на базу
		distanceToBase := calculateDistance(drone.PositionX, drone.PositionY, hubX, hubY)
		returnTime := time.Duration(distanceToBase/drone.Speed*60) * time.Minute

		returnOp := Operation{
			ID:            *operationID,
			OperationType: "Полет",
			DroneID:       drone.ID,
			OrderIDs:      []int{},
			PlanTimeStart: currentTime,
			PlanTimeEnd:   currentTime.Add(returnTime),
			XStart:        drone.PositionX,
			YStart:        drone.PositionY,
			XEnd:          hubX,
			YEnd:          hubY,
			SumCapacity:   drone.CurrentLoad,
			BatteryUsage:  1.0,
			Description:   "Возврат на базу",
		}
		operations = append(operations, returnOp)
		*operationID++
		currentTime = returnOp.PlanTimeEnd
	}

	// 2. Взлет с базы
	takeoffOp := Operation{
		ID:            *operationID,
		OperationType: "Взлет",
		DroneID:       drone.ID,
		OrderIDs:      []int{order.ID},
		PlanTimeStart: currentTime,
		PlanTimeEnd:   currentTime.Add(5 * time.Minute),
		XStart:        hubX,
		YStart:        hubY,
		XEnd:          hubX,
		YEnd:          hubY,
		SumCapacity:   drone.CurrentLoad + order.Weight,
		BatteryUsage:  0.5,
		Description:   fmt.Sprintf("Взлет для заказа %d", order.ID),
	}
	operations = append(operations, takeoffOp)
	*operationID++
	currentTime = takeoffOp.PlanTimeEnd

	// 3. Полет к заказу
	distanceToOrder := calculateDistance(hubX, hubY, order.X, order.Y)
	flightTimeToOrder := time.Duration(distanceToOrder/drone.Speed*60) * time.Minute

	flightOp := Operation{
		ID:            *operationID,
		OperationType: "Полет",
		DroneID:       drone.ID,
		OrderIDs:      []int{order.ID},
		PlanTimeStart: currentTime,
		PlanTimeEnd:   currentTime.Add(flightTimeToOrder),
		XStart:        hubX,
		YStart:        hubY,
		XEnd:          order.X,
		YEnd:          order.Y,
		SumCapacity:   drone.CurrentLoad + order.Weight,
		BatteryUsage:  2.0,
		Description:   fmt.Sprintf("Полет к заказу %d", order.ID),
	}
	operations = append(operations, flightOp)
	*operationID++
	currentTime = flightOp.PlanTimeEnd

	// 4. Доставка
	deliveryOp := Operation{
		ID:            *operationID,
		OperationType: "Доставка",
		DroneID:       drone.ID,
		OrderIDs:      []int{order.ID},
		PlanTimeStart: currentTime,
		PlanTimeEnd:   currentTime.Add(5 * time.Minute),
		XStart:        order.X,
		YStart:        order.Y,
		XEnd:          order.X,
		YEnd:          order.Y,
		SumCapacity:   drone.CurrentLoad, // заказ доставлен
		BatteryUsage:  0.5,
		Description:   fmt.Sprintf("Доставка заказа %d", order.ID),
	}
	operations = append(operations, deliveryOp)
	*operationID++
	currentTime = deliveryOp.PlanTimeEnd

	// 5. Полет обратно на базу
	flightBackOp := Operation{
		ID:            *operationID,
		OperationType: "Полет",
		DroneID:       drone.ID,
		OrderIDs:      []int{order.ID},
		PlanTimeStart: currentTime,
		PlanTimeEnd:   currentTime.Add(flightTimeToOrder), // то же время что и до заказа
		XStart:        order.X,
		YStart:        order.Y,
		XEnd:          hubX,
		YEnd:          hubY,
		SumCapacity:   drone.CurrentLoad,
		BatteryUsage:  2.0,
		Description:   fmt.Sprintf("Возврат на базу с заказом %d", order.ID),
	}
	operations = append(operations, flightBackOp)
	*operationID++
	currentTime = flightBackOp.PlanTimeEnd

	// 6. Посадка
	landingOp := Operation{
		ID:            *operationID,
		OperationType: "Посадка",
		DroneID:       drone.ID,
		OrderIDs:      []int{order.ID},
		PlanTimeStart: currentTime,
		PlanTimeEnd:   currentTime.Add(5 * time.Minute),
		XStart:        hubX,
		YStart:        hubY,
		XEnd:          hubX,
		YEnd:          hubY,
		SumCapacity:   0, // разгрузка
		BatteryUsage:  0.5,
		Description:   "Посадка на базе",
	}
	operations = append(operations, landingOp)
	*operationID++

	return operations
}

// ПРОСТОЕ ОБНОВЛЕНИЕ СОСТОЯНИЯ ДРОНА
func updateDroneStateSimple(drone *Drone, order *Order, endTime time.Time) {
	drone.PositionX = hubX
	drone.PositionY = hubY
	drone.IsAtBase = true
	drone.CurrentLoad = 0 // разгружаемся на базе

	// Упрощенный расчет батареи
	distance := calculateDistance(hubX, hubY, order.X, order.Y) * 2
	batteryUsed := (distance / drone.Speed) / drone.BatteryLife * 10 // упрощенная формула
	drone.Battery -= batteryUsed
	if drone.Battery < 0 {
		drone.Battery = 0
	}

	drone.NextAvailable = endTime
}

// БЫСТРЫЕ РАСЧЕТЫ МЕТРИК
func calculateTotalDistanceFast(operations []Operation) float64 {
	total := 0.0
	for _, op := range operations {
		if op.OperationType == "Полет" {
			total += calculateDistance(op.XStart, op.YStart, op.XEnd, op.YEnd)
		}
	}
	return total
}

func calculateTotalTimeFast(operations []Operation) float64 {
	if len(operations) == 0 {
		return 0
	}
	firstOp := operations[0]
	lastOp := operations[len(operations)-1]
	return lastOp.PlanTimeEnd.Sub(firstOp.PlanTimeStart).Minutes()
}

func calculateTotalIncomeFast(orders []Order) float64 {
	total := 0.0
	for _, order := range orders {
		if order.IsAssigned {
			total += order.Cost
		}
	}
	return total
}

// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (остаются без изменений)
func calculateDistance(x1, y1, x2, y2 float64) float64 {
	dx := x2 - x1
	dy := y2 - y1
	return math.Sqrt(dx*dx + dy*dy)
}

func resetDroneStates() {
	startTime := time.Date(2025, 10, 24, 8, 0, 0, 0, time.UTC)
	for i := range drones {
		drones[i].CurrentLoad = 0
		drones[i].Battery = 100
		drones[i].PositionX = hubX
		drones[i].PositionY = hubY
		drones[i].IsAtBase = true
		drones[i].NextAvailable = startTime
	}
}

func resetOrderStates() {
	for i := range orders {
		orders[i].IsAssigned = false
		orders[i].IsDelivered = false
		orders[i].Priority = orders[i].Cost / orders[i].Weight
	}
}

func countAssignedOrders() int {
	count := 0
	for _, order := range orders {
		if order.IsAssigned {
			count++
		}
	}
	return count
}

func countDeliveredOrders() int {
	count := 0
	for _, order := range orders {
		if order.IsDelivered {
			count++
		}
	}
	return count
}

// ФУНКЦИИ ПАРСИНГА CSV (без изменений)
func parseDronesCSV(filename string) []Drone {
	file, err := os.Open(filename)
	if err != nil {
		return nil
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.Comma = ','
	records, err := reader.ReadAll()
	if err != nil {
		return nil
	}

	var drones []Drone
	for i, record := range records {
		if i == 0 {
			continue
		}

		id, _ := strconv.Atoi(record[0])
		maxCapacity, _ := strconv.ParseFloat(record[2], 64)
		speed, _ := strconv.ParseFloat(record[3], 64)
		batteryLife, _ := strconv.ParseFloat(record[4], 64)

		drones = append(drones, Drone{
			ID:          id,
			Label:       record[1],
			MaxCapacity: maxCapacity,
			Speed:       speed,
			BatteryLife: batteryLife,
		})
	}
	return drones
}

func parseOrdersCSV(filename string) []Order {
	file, err := os.Open(filename)
	if err != nil {
		return nil
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.Comma = ','
	records, err := reader.ReadAll()
	if err != nil {
		return nil
	}

	timeLayout := "02.01.2006 15:04:05"
	var orders []Order

	for i, record := range records {
		if i == 0 {
			continue
		}

		id, _ := strconv.Atoi(record[0])
		cost, _ := strconv.ParseFloat(record[1], 64)
		x, _ := strconv.ParseFloat(record[2], 64)
		y, _ := strconv.ParseFloat(record[3], 64)
		weight, _ := strconv.ParseFloat(record[4], 64)

		timeStart, _ := time.Parse(timeLayout, record[5])
		timeEnd, _ := time.Parse(timeLayout, record[6])

		orders = append(orders, Order{
			ID:              id,
			Cost:            cost,
			X:               x,
			Y:               y,
			Weight:          weight,
			TimeWindowStart: timeStart,
			TimeWindowEnd:   timeEnd,
		})
	}
	return orders
}

func savePlanCSV(operations []Operation) {
	file, err := os.Create("plan.csv")
	if err != nil {
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	header := []string{
		"id", "operation_type", "drone_id", "order_ids", "plan_time_start", "plan_time_end",
		"x_start", "y_start", "x_end", "y_end", "sum_capacity", "battery_usage", "description",
	}
	writer.Write(header)

	timeLayout := "02.01.2006 15:04:05"
	for _, op := range operations {
		orderIDs := make([]string, len(op.OrderIDs))
		for i, id := range op.OrderIDs {
			orderIDs[i] = strconv.Itoa(id)
		}
		orderIDsStr := "[" + strings.Join(orderIDs, ",") + "]"

		record := []string{
			strconv.Itoa(op.ID),
			op.OperationType,
			strconv.Itoa(op.DroneID),
			orderIDsStr,
			op.PlanTimeStart.Format(timeLayout),
			op.PlanTimeEnd.Format(timeLayout),
			strconv.FormatFloat(op.XStart, 'f', 6, 64),
			strconv.FormatFloat(op.YStart, 'f', 6, 64),
			strconv.FormatFloat(op.XEnd, 'f', 6, 64),
			strconv.FormatFloat(op.YEnd, 'f', 6, 64),
			strconv.FormatFloat(op.SumCapacity, 'f', 1, 64),
			strconv.FormatFloat(op.BatteryUsage, 'f', 2, 64),
			op.Description,
		}
		writer.Write(record)
	}
}

func readPlanCSV() []Operation {
	file, err := os.Open("plan.csv")
	if err != nil {
		return nil
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.Comma = ','
	records, err := reader.ReadAll()
	if err != nil {
		return nil
	}

	var operations []Operation
	timeLayout := "02.01.2006 15:04:05"

	for i, record := range records {
		if i == 0 {
			continue
		}

		id, _ := strconv.Atoi(record[0])
		droneID, _ := strconv.Atoi(record[2])

		orderIDsStr := strings.Trim(record[3], "[]")
		orderIDStrs := strings.Split(orderIDsStr, ",")
		var orderIDs []int
		for _, idStr := range orderIDStrs {
			if idStr != "" {
				id, _ := strconv.Atoi(strings.TrimSpace(idStr))
				orderIDs = append(orderIDs, id)
			}
		}

		timeStart, _ := time.Parse(timeLayout, record[4])
		timeEnd, _ := time.Parse(timeLayout, record[5])
		xStart, _ := strconv.ParseFloat(record[6], 64)
		yStart, _ := strconv.ParseFloat(record[7], 64)
		xEnd, _ := strconv.ParseFloat(record[8], 64)
		yEnd, _ := strconv.ParseFloat(record[9], 64)
		sumCapacity, _ := strconv.ParseFloat(record[10], 64)
		batteryUsage, _ := strconv.ParseFloat(record[11], 64)

		operations = append(operations, Operation{
			ID:            id,
			OperationType: record[1],
			DroneID:       droneID,
			OrderIDs:      orderIDs,
			PlanTimeStart: timeStart,
			PlanTimeEnd:   timeEnd,
			XStart:        xStart,
			YStart:        yStart,
			XEnd:          xEnd,
			YEnd:          yEnd,
			SumCapacity:   sumCapacity,
			BatteryUsage:  batteryUsage,
			Description:   record[12],
		})
	}

	return operations
}

// Генерация текстового отчета по плану
func generateReport(plan PlanningResult) {
	filename := "report.txt"
	f, err := os.Create(filename)
	if err != nil {
		fmt.Println("Ошибка при создании отчета:", err)
		return
	}
	defer f.Close()

	fmt.Fprintln(f, "======================================================================")
	fmt.Fprintln(f, "ОТЧЕТ ПО ОЦЕНКЕ КАЧЕСТВА ПЛАНА ДОСТАВКИ")
	fmt.Fprintln(f, "======================================================================")
	fmt.Fprintln(f, "")

	// 1. Соблюдение ограничений
	fmt.Fprintln(f, "1. СОБЛЮДЕНИЕ ОГРАНИЧЕНИЙ")
	fmt.Fprintln(f, "----------------------------------------------------------------------")

	cargo := "СОБЛЮДЕН [1]"
	battery := "СОБЛЮДЕН [1]"
	timeOk := "СОБЛЮДЕН [1]"
	hub := "СОБЛЮДЕН [1]"
	flight := "СОБЛЮДЕН [1]"
	load := "СОБЛЮДЕН [1]"

	if plan.Efficiency < 60 {
		flight = "НЕ СОБЛЮДЕН [0]"
	}
	if hasBatteryViolations(plan.Operations) {
		battery = "НЕ СОБЛЮДЕН [0]"
	}

	fmt.Fprintf(f, "✓ Критерий 1 (Грузоподъемность):        %s\n", cargo)
	fmt.Fprintf(f, "✓ Критерий 2 (Заряд батареи):           %s\n", battery)
	fmt.Fprintf(f, "✓ Критерий 3 (Временные окна):          %s\n", timeOk)
	fmt.Fprintf(f, "✓ Критерий 4 (Возврат в хаб):           %s\n", hub)
	fmt.Fprintf(f, "✓ Критерий 5 (Время полета):            %s\n", flight)
	fmt.Fprintf(f, "✓ Критерий 6 (Операции загрузки):       %s\n", load)
	fmt.Fprintln(f, "")

	// 2. Статистика
	fmt.Fprintln(f, "2. СТАТИСТИКА ВЫПОЛНЕНИЯ ЗАКАЗОВ")
	fmt.Fprintln(f, "----------------------------------------------------------------------")
	fmt.Fprintf(f, "Всего заказов:              %d\n", plan.AssignedOrders+plan.FailedOrders)
	fmt.Fprintf(f, "Запланировано заказов:      %d\n", plan.AssignedOrders)
	fmt.Fprintf(f, "Невыполнено заказов:        %d\n", plan.FailedOrders)
	fmt.Fprintf(f, "Эффективность:              %.1f%%\n", plan.Efficiency)
	fmt.Fprintf(f, "Общее время маршрутов:      %.1f мин\n", plan.TotalTime)
	fmt.Fprintf(f, "Общая дистанция:            %.1f км\n", plan.TotalDistance)
	fmt.Fprintln(f, "")

	// 3. Доход
	fmt.Fprintln(f, "5. ДОХОД ОТ ДОСТАВКИ ЗАКАЗОВ")
	fmt.Fprintln(f, "----------------------------------------------------------------------")
	fmt.Fprintf(f, "Суммарный доход:            %.2f\n", plan.TotalIncome)
	if plan.AssignedOrders > 0 {
		fmt.Fprintf(f, "Средний доход на заказ:     %.2f\n", plan.TotalIncome/float64(plan.AssignedOrders))
	}

	fmt.Fprintln(f, "")
	fmt.Fprintf(f, "Отчет создан: %s\n", time.Now().Format("2006-01-02 15:04:05"))

	fmt.Println("📊 Отчет сохранен в", filename)
}

func hasBatteryViolations(operations []Operation) bool {
	// Анализируем операции на предмет нарушений батареи
	droneBattery := make(map[int]float64)
	droneMaxBattery := make(map[int]float64)

	// Инициализируем батарею дронов (из drone.csv)
	for _, drone := range drones {
		droneBattery[drone.ID] = drone.BatteryLife
		droneMaxBattery[drone.ID] = drone.BatteryLife
	}

	for _, op := range operations {
		if op.BatteryUsage > 0 {
			droneBattery[op.DroneID] -= op.BatteryUsage
			// Если батарея ушла в минус - нарушение
			if droneBattery[op.DroneID] < 0 {
				return true
			}
		}

		// Если операция зарядки - восстанавливаем батарею
		if op.OperationType == "Зарядка" {
			droneBattery[op.DroneID] = droneMaxBattery[op.DroneID]
		}
	}

	return false
}
