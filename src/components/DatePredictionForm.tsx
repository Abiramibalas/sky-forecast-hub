import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Calendar, Clock } from "lucide-react";
import { toast } from "sonner";
import AQICard from "./AQICard";

interface DatePredictionData {
  date: string;
}

const DatePredictionForm = () => {
  const [dateData, setDateData] = useState<DatePredictionData>({
    date: "",
  });

  const [prediction, setPrediction] = useState<{
    aqi: number;
    category: string;
    explanation?: string;
    estimated_conditions?: any;
    date?: string;
  } | null>(null);

  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDateData({ ...dateData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Validate date
    if (!dateData.date) {
      toast.error("Please select a date");
      setIsLoading(false);
      return;
    }

    // Validate date format and range
    const selectedDate = new Date(dateData.date);
    const today = new Date();
    const minDate = new Date("2020-01-01");
    const maxDate = new Date("2030-12-31");

    if (selectedDate < minDate || selectedDate > maxDate) {
      toast.error("Please select a date between 2020 and 2030");
      setIsLoading(false);
      return;
    }

    try {
      // Call the backend API for date-based prediction
      const response = await fetch("http://127.0.0.1:8000/predict-by-date", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          date: dateData.date
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.error) {
        toast.error(result.error);
        return;
      }

      setPrediction({ 
        aqi: result.predicted_AQI, 
        category: result.category,
        explanation: result.explanation,
        estimated_conditions: result.estimated_conditions,
        date: result.date
      });
      toast.success("Date-based AQI prediction generated successfully!");
    } catch (error) {
      console.error("Prediction error:", error);
      toast.error("Failed to get prediction. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section id="date-predict" className="py-16 px-4 bg-muted/30">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-12 animate-fade-in">
          <h2 className="text-4xl font-bold mb-4 text-foreground">
            Predict Air Quality by Date
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Enter a specific date to get AQI predictions based on seasonal patterns and historical data
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <Card className="p-6 shadow-lg animate-slide-in">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="date" className="flex items-center gap-2 mb-2">
                  <Calendar className="h-4 w-4 text-primary" />
                  Select Date
                </Label>
                <Input
                  id="date"
                  name="date"
                  type="date"
                  value={dateData.date}
                  onChange={handleChange}
                  min="2020-01-01"
                  max="2030-12-31"
                  className="transition-all focus:ring-2 focus:ring-primary"
                />
                <p className="text-sm text-muted-foreground mt-2">
                  Choose any date between 2020-2030 for seasonal prediction
                </p>
              </div>

              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-primary to-secondary hover:shadow-lg transition-all"
                disabled={isLoading}
              >
                {isLoading ? "Predicting..." : "Predict AQI by Date"}
              </Button>
            </form>
          </Card>

          <div className="animate-slide-in" style={{ animationDelay: "0.2s" }}>
            {prediction ? (
              <div className="space-y-4">
                <AQICard 
                  aqi={prediction.aqi} 
                  category={prediction.category} 
                  explanation={prediction.explanation}
                />
                
                {prediction.estimated_conditions && (
                  <Card className="p-6 bg-gradient-to-br from-card to-muted/50">
                    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                      <Clock className="h-5 w-5 text-primary" />
                      Estimated Conditions for {prediction.date}
                    </h3>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-muted-foreground">Temperature:</span>
                        <span className="ml-2 font-medium">{prediction.estimated_conditions.Temperature}°C</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Humidity:</span>
                        <span className="ml-2 font-medium">{prediction.estimated_conditions.Humidity}%</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Wind Speed:</span>
                        <span className="ml-2 font-medium">{prediction.estimated_conditions.WindSpeed} m/s</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">NO2:</span>
                        <span className="ml-2 font-medium">{prediction.estimated_conditions.NO2} µg/m³</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">CO:</span>
                        <span className="ml-2 font-medium">{prediction.estimated_conditions.CO} mg/m³</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">PM2.5:</span>
                        <span className="ml-2 font-medium">{prediction.estimated_conditions.PM25} µg/m³</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">PM10:</span>
                        <span className="ml-2 font-medium">{prediction.estimated_conditions.PM10} µg/m³</span>
                      </div>
                    </div>
                  </Card>
                )}
              </div>
            ) : (
              <Card className="p-8 h-full flex items-center justify-center bg-gradient-to-br from-card to-muted/50">
                <div className="text-center">
                  <Calendar className="h-16 w-16 text-muted-foreground mx-auto mb-4 animate-float" />
                  <p className="text-muted-foreground text-lg">
                    Your date-based AQI prediction will appear here
                  </p>
                </div>
              </Card>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

export default DatePredictionForm;
