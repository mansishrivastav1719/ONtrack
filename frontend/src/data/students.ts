export type RiskLevel = "Low" | "Medium" | "High";

export interface Student {
  id: string;
  name: string;
  semester: number;
  gpa: number;
  attendance: number;
  riskLevel: RiskLevel;
  riskScore: number;
  department: string;
  email: string;
}

export const mockStudents: Student[] = [
  { id: "STU001", name: "Aarav Sharma", semester: 4, gpa: 3.8, attendance: 92, riskLevel: "Low", riskScore: 12, department: "Computer Science", email: "aarav@uni.edu" },
  { id: "STU002", name: "Priya Patel", semester: 3, gpa: 2.1, attendance: 58, riskLevel: "High", riskScore: 87, department: "Mathematics", email: "priya@uni.edu" },
  { id: "STU003", name: "Rahul Verma", semester: 6, gpa: 2.9, attendance: 71, riskLevel: "Medium", riskScore: 52, department: "Physics", email: "rahul@uni.edu" },
  { id: "STU004", name: "Sneha Gupta", semester: 2, gpa: 3.5, attendance: 88, riskLevel: "Low", riskScore: 18, department: "Computer Science", email: "sneha@uni.edu" },
  { id: "STU005", name: "Vikram Singh", semester: 5, gpa: 1.8, attendance: 45, riskLevel: "High", riskScore: 93, department: "Engineering", email: "vikram@uni.edu" },
  { id: "STU006", name: "Ananya Reddy", semester: 4, gpa: 3.2, attendance: 82, riskLevel: "Low", riskScore: 22, department: "Biology", email: "ananya@uni.edu" },
  { id: "STU007", name: "Karan Mehta", semester: 3, gpa: 2.4, attendance: 63, riskLevel: "Medium", riskScore: 61, department: "Chemistry", email: "karan@uni.edu" },
  { id: "STU008", name: "Divya Nair", semester: 7, gpa: 2.0, attendance: 50, riskLevel: "High", riskScore: 85, department: "Mathematics", email: "divya@uni.edu" },
  { id: "STU009", name: "Arjun Das", semester: 2, gpa: 3.6, attendance: 90, riskLevel: "Low", riskScore: 10, department: "Computer Science", email: "arjun@uni.edu" },
  { id: "STU010", name: "Meera Joshi", semester: 5, gpa: 2.7, attendance: 68, riskLevel: "Medium", riskScore: 48, department: "Physics", email: "meera@uni.edu" },
  { id: "STU011", name: "Rohan Kapoor", semester: 6, gpa: 1.9, attendance: 42, riskLevel: "High", riskScore: 91, department: "Engineering", email: "rohan@uni.edu" },
  { id: "STU012", name: "Ishita Banerjee", semester: 3, gpa: 3.4, attendance: 85, riskLevel: "Low", riskScore: 15, department: "Biology", email: "ishita@uni.edu" },
  { id: "STU013", name: "Aditya Rao", semester: 4, gpa: 2.5, attendance: 66, riskLevel: "Medium", riskScore: 55, department: "Chemistry", email: "aditya@uni.edu" },
  { id: "STU014", name: "Pooja Mishra", semester: 8, gpa: 2.2, attendance: 55, riskLevel: "High", riskScore: 78, department: "Mathematics", email: "pooja@uni.edu" },
  { id: "STU015", name: "Nikhil Kumar", semester: 2, gpa: 3.9, attendance: 95, riskLevel: "Low", riskScore: 5, department: "Computer Science", email: "nikhil@uni.edu" },
];

export const trendData = [
  { semester: "Sem 1", low: 60, medium: 25, high: 15 },
  { semester: "Sem 2", low: 55, medium: 28, high: 17 },
  { semester: "Sem 3", low: 50, medium: 30, high: 20 },
  { semester: "Sem 4", low: 48, medium: 29, high: 23 },
  { semester: "Sem 5", low: 45, medium: 30, high: 25 },
  { semester: "Sem 6", low: 42, medium: 32, high: 26 },
  { semester: "Sem 7", low: 40, medium: 30, high: 30 },
  { semester: "Sem 8", low: 38, medium: 30, high: 32 },
];

export const departmentRisk = [
  { department: "Computer Science", low: 4, medium: 0, high: 0 },
  { department: "Mathematics", low: 0, medium: 0, high: 2 },
  { department: "Physics", low: 0, medium: 1, high: 0 },
  { department: "Engineering", low: 0, medium: 0, high: 2 },
  { department: "Biology", low: 2, medium: 0, high: 0 },
  { department: "Chemistry", low: 0, medium: 2, high: 0 },
];
