
-- Query 1: Night Shift Crisis Analysis (SLIDE 7)
-- Validates 45% defect concentration in night shift
SELECT 
    shift,
    COUNT(*) as total_defects,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage,
    ROUND(AVG(defect_cost_pln), 2) as avg_cost_pln,
    ROUND(SUM(defect_cost_pln), 2) as total_cost_pln
FROM manufacturing_defects
GROUP BY shift
ORDER BY total_defects DESC;

-- Query 2: Pareto Analysis - Top 3 Defects (SLIDE 9)
-- Confirms 82% of costs from top 3 defect types
SELECT 
    defect_type,
    SUM(defect_cost_pln) as total_cost,
    ROUND(SUM(defect_cost_pln) * 100.0 / 
          (SELECT SUM(defect_cost_pln) FROM manufacturing_defects), 1) as cost_percentage,
    ROUND(SUM(SUM(defect_cost_pln)) OVER (ORDER BY SUM(defect_cost_pln) DESC) * 100.0 /
          (SELECT SUM(defect_cost_pln) FROM manufacturing_defects), 1) as cumulative_percentage
FROM manufacturing_defects
GROUP BY defect_type
ORDER BY total_cost DESC;

-- Query 3: Machine Root Cause Analysis (SLIDE 11)
-- Identifies M002 as highest cost machine
SELECT 
    machine_id,
    COUNT(*) as defect_count,
    ROUND(AVG(defect_cost_pln), 2) as avg_cost,
    ROUND(SUM(defect_cost_pln), 2) as total_cost,
    ROUND(STDDEV(defect_cost_pln), 2) as cost_std_dev
FROM manufacturing_defects
GROUP BY machine_id
ORDER BY avg_cost DESC;

-- Query 4: Resolution Rate by Defect Type
SELECT 
    defect_type,
    COUNT(*) as total_defects,
    SUM(CASE WHEN is_resolved THEN 1 ELSE 0 END) as resolved_count,
    ROUND(AVG(CASE WHEN is_resolved THEN 1.0 ELSE 0.0 END) * 100, 1) as resolution_rate_pct
FROM manufacturing_defects
GROUP BY defect_type
ORDER BY resolution_rate_pct DESC;

-- Query 5: Shift-Severity Heat Map Data
SELECT 
    shift,
    severity,
    COUNT(*) as defect_count,
    ROUND(AVG(defect_cost_pln), 2) as avg_cost
FROM manufacturing_defects
GROUP BY shift, severity
ORDER BY shift, severity;

-- Query 6: Daily Trend Analysis
SELECT 
    DATE(timestamp) as defect_date,
    COUNT(*) as daily_defects,
    SUM(defect_cost_pln) as daily_cost
FROM manufacturing_defects
GROUP BY DATE(timestamp)
ORDER BY defect_date;

-- Query 7: Operator Performance (for 8D analysis)
SELECT 
    operator_id,
    COUNT(*) as defect_count,
    ROUND(AVG(defect_cost_pln), 2) as avg_defect_cost,
    COUNT(DISTINCT machine_id) as machines_operated
FROM manufacturing_defects
GROUP BY operator_id
HAVING COUNT(*) > 20
ORDER BY defect_count DESC
LIMIT 10;
