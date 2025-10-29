import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Thermometer, Droplets, Wind, Activity } from "lucide-react";
import { toast } from "sonner";
import AQICard from "./AQICard";

interface FormData {
  temperature: string;
  humidity: string;
  windSpeed: string;
  no2: string;
  co: string;
  pm25: string;
  pm10: string;
}

const PredictionForm = () => {
  const [formData, setFormData] = useState<FormData>({
    temperature: "",
    humidity: "",
    windSpeed: "",
    no2: "",
    co: "",
    pm25: "",
    pm10: "",
  });

  const [prediction, setPrediction] = useState<{
    aqi: number;
    category: string;
    explanation?: string;
  } | null>(null);

  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Validate inputs
    const values = Object.values(formData);
    if (values.some((val) => val === "" || isNaN(Number(val)))) {
      toast.error("Please fill in all fields with valid numbers");
      setIsLoading(false);
      return;
    }

    try {
      // Call the backend API
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          Temperature: Number(formData.temperature),
          Humidity: Number(formData.humidity),
          WindSpeed: Number(formData.windSpeed),
          NO2: Number(formData.no2),
          CO: Number(formData.co),
          PM25: Number(formData.pm25),
          PM10: Number(formData.pm10)
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setPrediction({ 
        aqi: result.predicted_AQI, 
        category: result.category,
        explanation: result.explanation
      });
      toast.success("AQI prediction generated successfully!");
    } catch (error) {
      console.error("Prediction error:", error);
      toast.error("Failed to get prediction. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const inputFields = [
    {
      name: "temperature",
      label: "Temperature (°C)",
      icon: Thermometer,
      placeholder: "25.5",
    },
    {
      name: "humidity",
      label: "Humidity (%)",
      icon: Droplets,
      placeholder: "65",
    },
    {
      name: "windSpeed",
      label: "Wind Speed (m/s)",
      icon: Wind,
      placeholder: "3.5",
    },
    { name: "no2", label: "NO₂ (µg/m³)", icon: Activity, placeholder: "40" },
    { name: "co", label: "CO (mg/m³)", icon: Activity, placeholder: "1.2" },
    { name: "pm25", label: "PM2.5 (µg/m³)", icon: Activity, placeholder: "35" },
    { name: "pm10", label: "PM10 (µg/m³)", icon: Activity, placeholder: "50" },
  ];

  return (
    <section id="predict" className="py-16 px-4 bg-muted/30">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-12 animate-fade-in">
          <h2 className="text-4xl font-bold mb-4 text-foreground">
            Predict Air Quality
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Enter weather and pollutant data to get instant AQI predictions
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          <Card className="p-6 shadow-lg animate-slide-in">
            <form onSubmit={handleSubmit} className="space-y-4">
              {inputFields.map((field) => {
                const Icon = field.icon;
                return (
                  <div key={field.name}>
                    <Label htmlFor={field.name} className="flex items-center gap-2 mb-2">
                      <Icon className="h-4 w-4 text-primary" />
                      {field.label}
                    </Label>
                    <Input
                      id={field.name}
                      name={field.name}
                      type="number"
                      step="0.01"
                      placeholder={field.placeholder}
                      value={formData[field.name as keyof FormData]}
                      onChange={handleChange}
                      className="transition-all focus:ring-2 focus:ring-primary"
                    />
                  </div>
                );
              })}

              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-primary to-secondary hover:shadow-lg transition-all"
                disabled={isLoading}
              >
                {isLoading ? "Predicting..." : "Predict AQI"}
              </Button>
            </form>
          </Card>

          <div className="animate-slide-in" style={{ animationDelay: "0.2s" }}>
            {prediction ? (
              <AQICard 
                aqi={prediction.aqi} 
                category={prediction.category} 
                explanation={prediction.explanation}
              />
            ) : (
              <Card className="p-8 h-full flex items-center justify-center bg-gradient-to-br from-card to-muted/50">
                <div className="text-center">
                  <Activity className="h-16 w-16 text-muted-foreground mx-auto mb-4 animate-float" />
                  <p className="text-muted-foreground text-lg">
                    Your AQI prediction will appear here
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

export default PredictionForm;
