import Dexie from 'dexie';

export const db = new Dexie('FaithSchoolDB');

db.version(1).stores({
  students: 'id, admission_number, class_id',
  attendance: '++id, student_id, date, synced',
  classes: 'id, name, grade_level',
  invoices: 'id, invoice_number, student_id, status',
  announcements: 'id, posted_at',
  syncQueue: '++id, type, data, timestamp'
});

export async function saveAttendanceOffline(attendanceData) {
  await db.attendance.add({
    ...attendanceData,
    synced: false,
    timestamp: Date.now()
  });
  
  await db.syncQueue.add({
    type: 'attendance',
    data: attendanceData,
    timestamp: Date.now()
  });
}

export async function syncPendingData(api) {
  const pending = await db.syncQueue.toArray();
  
  for (const item of pending) {
    try {
      if (item.type === 'attendance') {
        await api.post('/api/attendance/', item.data);
        await db.syncQueue.delete(item.id);
        
        const attendanceRecords = await db.attendance
          .where('student_id').equals(item.data.student_id)
          .and(record => record.date === item.data.date)
          .toArray();
        
        for (const record of attendanceRecords) {
          await db.attendance.update(record.id, { synced: true });
        }
      }
    } catch (error) {
      console.error('Sync failed for item:', item, error);
    }
  }
  
  return pending.length;
}

export async function getPendingSyncCount() {
  return await db.syncQueue.count();
}
