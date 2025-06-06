import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, ResponsiveContainer, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { ArrowUpRight, ArrowDownRight, Wifi, Signal, AlertTriangle, ExternalLink } from 'lucide-react';
import api from '@/services/api';

/**
 * Client dashboard page component
 * @returns {JSX.Element} DashboardPage component
 */
export default function DashboardPage() {
  const [stats, setStats] = useState({
    dataUsed: 0,
    dataLimit: 100,
    uptime: 98.5,
    signalQuality: 85,
    activeAlerts: 0,
  });
  
  const [usageData, setUsageData] = useState([]);
  const [speedData, setSpeedData] = useState([]);
  const [latencyData, setLatencyData] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        // In a real application, we would fetch this data from the API
        // For now, we'll use mock data
        
        // Mock usage statistics
        const usageStats = {
          dataUsed: 45.8,
          dataLimit: 100,
          uptime: 98.5,
          signalQuality: 85,
          activeAlerts: 2,
        };
        
        setStats(usageStats);
        
        // Mock usage data for the past 7 days
        setUsageData([
          { name: 'Mon', download: 5.2, upload: 1.8 },
          { name: 'Tue', download: 4.8, upload: 1.5 },
          { name: 'Wed', download: 6.3, upload: 2.1 },
          { name: 'Thu', download: 5.7, upload: 1.9 },
          { name: 'Fri', download: 7.1, upload: 2.4 },
          { name: 'Sat', download: 8.5, upload: 3.2 },
          { name: 'Sun', download: 6.9, upload: 2.3 },
        ]);
        
        // Mock speed data
        setSpeedData([
          { time: '00:00', download: 120, upload: 15 },
          { time: '04:00', download: 90, upload: 12 },
          { time: '08:00', download: 70, upload: 10 },
          { time: '12:00', download: 110, upload: 14 },
          { time: '16:00', download: 150, upload: 18 },
          { time: '20:00', download: 180, upload: 20 },
          { time: '23:59', download: 130, upload: 16 },
        ]);
        
        // Mock latency data
        setLatencyData([
          { time: '00:00', latency: 35 },
          { time: '04:00', latency: 32 },
          { time: '08:00', latency: 45 },
          { time: '12:00', latency: 50 },
          { time: '16:00', latency: 40 },
          { time: '20:00', latency: 38 },
          { time: '23:59', latency: 36 },
        ]);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);
  
  // Calculate percentage of data used
  const dataUsedPercentage = (stats.dataUsed / stats.dataLimit) * 100;
  
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">Welcome to your Starlink dashboard.</p>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Data Usage</CardTitle>
            <div className="flex items-center space-x-1">
              <ArrowDownRight className="h-4 w-4 text-muted-foreground" />
              <ArrowUpRight className="h-4 w-4 text-muted-foreground" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.dataUsed} GB</div>
            <Progress value={dataUsedPercentage} className="mt-2" />
            <p className="mt-2 text-xs text-muted-foreground">
              {stats.dataUsed} GB of {stats.dataLimit} GB used
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Uptime</CardTitle>
            <Wifi className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.uptime}%</div>
            <p className="text-xs text-muted-foreground">Last 30 days</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Signal Quality</CardTitle>
            <Signal className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.signalQuality}%</div>
            <Progress value={stats.signalQuality} className="mt-2" />
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Alerts</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.activeAlerts}</div>
            <p className="text-xs text-muted-foreground">
              {stats.activeAlerts > 0 ? 'Requires attention' : 'All systems normal'}
            </p>
          </CardContent>
        </Card>
      </div>
      
      <Tabs defaultValue="usage" className="space-y-4">
        <TabsList>
          <TabsTrigger value="usage">Usage</TabsTrigger>
          <TabsTrigger value="speed">Speed</TabsTrigger>
          <TabsTrigger value="latency">Latency</TabsTrigger>
        </TabsList>
        
        <TabsContent value="usage" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Daily Data Usage</CardTitle>
              <CardDescription>Data usage over the past 7 days (GB)</CardDescription>
            </CardHeader>
            <CardContent className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={usageData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="download" fill="var(--color-chart-1)" name="Download (GB)" />
                  <Bar dataKey="upload" fill="var(--color-chart-2)" name="Upload (GB)" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
            <CardFooter>
              <Button variant="outline" className="ml-auto" asChild>
                <div className="flex items-center">
                  <span>View detailed usage</span>
                  <ExternalLink className="ml-2 h-4 w-4" />
                </div>
              </Button>
            </CardFooter>
          </Card>
        </TabsContent>
        
        <TabsContent value="speed" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Speed Performance</CardTitle>
              <CardDescription>Average speeds over the past 24 hours (Mbps)</CardDescription>
            </CardHeader>
            <CardContent className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={speedData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area type="monotone" dataKey="download" stroke="var(--color-chart-1)" fill="var(--color-chart-1)" fillOpacity={0.2} name="Download (Mbps)" />
                  <Area type="monotone" dataKey="upload" stroke="var(--color-chart-2)" fill="var(--color-chart-2)" fillOpacity={0.2} name="Upload (Mbps)" />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="latency" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Latency</CardTitle>
              <CardDescription>Average latency over the past 24 hours (ms)</CardDescription>
            </CardHeader>
            <CardContent className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={latencyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="latency" stroke="var(--color-chart-3)" name="Latency (ms)" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

