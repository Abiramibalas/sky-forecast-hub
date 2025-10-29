import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import PredictionForm from "@/components/PredictionForm";
import DatePredictionForm from "@/components/DatePredictionForm";
import ChartSection from "@/components/ChartSection";
import About from "@/components/About";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <Hero />
      <PredictionForm />
      <DatePredictionForm />
      <ChartSection />
      <About />
    </div>
  );
};

export default Index;
