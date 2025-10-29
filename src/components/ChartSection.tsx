import { Card } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from "recharts";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { TrendingUp } from "lucide-react";

const ChartSection = () => {
  // Mock historical data
  const aqiTrendData = [
    { year: "2020", aqi: 85, pm25: 35, pm10: 58, no2: 42 },
    { year: "2021", aqi: 92, pm25: 38, pm10: 62, no2: 45 },
    { year: "2022", aqi: 78, pm25: 32, pm10: 54, no2: 38 },
    { year: "2023", aqi: 88, pm25: 36, pm10: 60, no2: 43 },
    { year: "2024", aqi: 82, pm25: 34, pm10: 56, no2: 40 },
  ];

  const pollutantComparison = [
    { pollutant: "PM2.5", "2020": 35, "2024": 34 },
    { pollutant: "PM10", "2020": 58, "2024": 56 },
    { pollutant: "NO₂", "2020": 42, "2024": 40 },
    { pollutant: "CO", "2020": 1.5, "2024": 1.3 },
  ];

  return (
    <section id="visualization" className="py-16 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-12 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full mb-4">
            <TrendingUp className="h-4 w-4 text-primary" />
            <span className="text-sm font-medium text-primary">Historical Trends</span>
          </div>
          <h2 className="text-4xl font-bold mb-4 text-foreground">
            Data Visualization
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Analyze air quality trends from 2020-2024
          </p>
        </div>

        <Tabs defaultValue="aqi" className="w-full">
          <TabsList className="grid w-full max-w-md mx-auto grid-cols-2 mb-8">
            <TabsTrigger value="aqi">AQI Trends</TabsTrigger>
            <TabsTrigger value="pollutants">Pollutant Comparison</TabsTrigger>
          </TabsList>

          <TabsContent value="aqi" className="animate-fade-in">
            <Card className="p-6 shadow-lg">
              <h3 className="text-xl font-semibold mb-4 text-foreground">
                AQI Trends Over Time
              </h3>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={aqiTrendData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis 
                    dataKey="year" 
                    stroke="hsl(var(--foreground))"
                  />
                  <YAxis stroke="hsl(var(--foreground))" />
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                    }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="aqi" 
                    stroke="hsl(var(--primary))" 
                    strokeWidth={3}
                    dot={{ fill: "hsl(var(--primary))", r: 5 }}
                    activeDot={{ r: 7 }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="pm25" 
                    stroke="hsl(var(--aqi-moderate))" 
                    strokeWidth={2}
                    name="PM2.5"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="pm10" 
                    stroke="hsl(var(--aqi-poor))" 
                    strokeWidth={2}
                    name="PM10"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="no2" 
                    stroke="hsl(var(--secondary))" 
                    strokeWidth={2}
                    name="NO₂"
                  />
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </TabsContent>

          <TabsContent value="pollutants" className="animate-fade-in">
            <Card className="p-6 shadow-lg">
              <h3 className="text-xl font-semibold mb-4 text-foreground">
                Pollutant Levels: 2020 vs 2024
              </h3>
              <ResponsiveContainer width="100%" height={400}>
                <BarChart data={pollutantComparison}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis 
                    dataKey="pollutant" 
                    stroke="hsl(var(--foreground))"
                  />
                  <YAxis stroke="hsl(var(--foreground))" />
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                    }}
                  />
                  <Legend />
                  <Bar 
                    dataKey="2020" 
                    fill="hsl(var(--primary))" 
                    radius={[8, 8, 0, 0]}
                  />
                  <Bar 
                    dataKey="2024" 
                    fill="hsl(var(--secondary))" 
                    radius={[8, 8, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </section>
  );
};

export default ChartSection;
