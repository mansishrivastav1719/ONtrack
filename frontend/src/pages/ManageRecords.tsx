import { useState, useMemo } from "react";
import { mockStudents, Student } from "@/data/students";
import { RiskBadge } from "@/components/RiskBadge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Search, Pencil, Trash2, Download } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function ManageRecords() {
  const [students, setStudents] = useState<Student[]>(mockStudents);
  const [search, setSearch] = useState("");
  const [editStudent, setEditStudent] = useState<Student | null>(null);
  const [editForm, setEditForm] = useState({ name: "", gpa: "", attendance: "" });
  const { toast } = useToast();

  const filtered = useMemo(() => {
    return students.filter(
      (s) =>
        s.name.toLowerCase().includes(search.toLowerCase()) ||
        s.id.toLowerCase().includes(search.toLowerCase())
    );
  }, [students, search]);

  const openEdit = (s: Student) => {
    setEditStudent(s);
    setEditForm({ name: s.name, gpa: s.gpa.toString(), attendance: s.attendance.toString() });
  };

  const saveEdit = () => {
    if (!editStudent) return;
    setStudents((prev) =>
      prev.map((s) =>
        s.id === editStudent.id
          ? { ...s, name: editForm.name, gpa: parseFloat(editForm.gpa), attendance: parseFloat(editForm.attendance) }
          : s
      )
    );
    setEditStudent(null);
    toast({ title: "Record updated", description: `${editForm.name} has been updated.` });
  };

  const deleteStudent = (id: string) => {
    setStudents((prev) => prev.filter((s) => s.id !== id));
    toast({ title: "Record deleted", description: `Student ${id} removed.`, variant: "destructive" });
  };

  const exportCSV = () => {
    const headers = "ID,Name,Semester,GPA,Attendance,Risk Level,Risk Score\n";
    const rows = students.map((s) => `${s.id},${s.name},${s.semester},${s.gpa},${s.attendance},${s.riskLevel},${s.riskScore}`).join("\n");
    const blob = new Blob([headers + rows], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "students_data.csv";
    a.click();
    URL.revokeObjectURL(url);
    toast({ title: "Exported", description: "CSV file downloaded." });
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Manage Records</h1>
          <p className="text-muted-foreground text-sm mt-1">View, edit, or delete student records</p>
        </div>
        <Button variant="outline" onClick={exportCSV}>
          <Download className="mr-2 h-4 w-4" /> Export CSV
        </Button>
      </div>

      <Card>
        <CardHeader className="pb-3">
          <div className="relative">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input placeholder="Search students..." value={search} onChange={(e) => setSearch(e.target.value)} className="pl-10" />
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-muted/50">
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">Name</th>
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">ID</th>
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">Dept</th>
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">GPA</th>
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">Attendance</th>
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">Risk</th>
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((s) => (
                  <tr key={s.id} className="border-b last:border-0 hover:bg-muted/30 transition-colors">
                    <td className="px-4 py-3 font-medium">{s.name}</td>
                    <td className="px-4 py-3 text-muted-foreground">{s.id}</td>
                    <td className="px-4 py-3 text-muted-foreground">{s.department}</td>
                    <td className="px-4 py-3">{s.gpa.toFixed(1)}</td>
                    <td className="px-4 py-3">{s.attendance}%</td>
                    <td className="px-4 py-3"><RiskBadge level={s.riskLevel} /></td>
                    <td className="px-4 py-3">
                      <div className="flex gap-1">
                        <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => openEdit(s)}>
                          <Pencil className="h-3.5 w-3.5" />
                        </Button>
                        <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive hover:text-destructive" onClick={() => deleteStudent(s.id)}>
                          <Trash2 className="h-3.5 w-3.5" />
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Edit Dialog */}
      <Dialog open={!!editStudent} onOpenChange={() => setEditStudent(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Student — {editStudent?.id}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-2">
            <div className="space-y-2">
              <label className="text-sm font-medium">Name</label>
              <Input value={editForm.name} onChange={(e) => setEditForm({ ...editForm, name: e.target.value })} />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">GPA</label>
              <Input type="number" step="0.1" value={editForm.gpa} onChange={(e) => setEditForm({ ...editForm, gpa: e.target.value })} />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Attendance (%)</label>
              <Input type="number" value={editForm.attendance} onChange={(e) => setEditForm({ ...editForm, attendance: e.target.value })} />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditStudent(null)}>Cancel</Button>
            <Button onClick={saveEdit}>Save Changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
