'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';
import { ReviewQueueItem } from '@/lib/types';

const statusColors = {
  pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  approved: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  rejected: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  deferred: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
};

export default function ReviewQueuePage() {
  const [items, setItems] = useState<ReviewQueueItem[]>([]);
  const [filter, setFilter] = useState('pending');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.getReviewQueue(filter === 'all' ? undefined : filter)
      .then(setItems)
      .catch(() => {
        // Fallback dummy data
        const dummy: ReviewQueueItem[] = [
          { id: '1', itemType: 'Camera', reason: 'User Reported', status: 'pending', createdDate: '2026-08-10', assignedTo: 'Unassigned' },
          { id: '2', itemType: 'Speed Limit', reason: 'Source Mismatch', status: 'approved', createdDate: '2026-08-11', assignedTo: 'Admin' },
          { id: '3', itemType: 'Traffic Signal', reason: 'Stale Data', status: 'deferred', createdDate: '2026-08-09', assignedTo: 'FieldTeamA' },
          { id: '4', itemType: 'Camera', reason: 'Disputed', status: 'rejected', createdDate: '2026-08-08', assignedTo: 'Admin' },
        ];
        setItems(filter === 'all' ? dummy : dummy.filter(i => i.status === filter));
      })
      .finally(() => setLoading(false));
  }, [filter]);

  return (
    <div className="space-y-6 dark:bg-gray-900 min-h-full p-6 dark:text-white">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Review Queue</h1>
        <div className="flex gap-2">
          {['all', 'pending', 'approved', 'rejected', 'deferred'].map(f => (
            <button 
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1 rounded text-sm capitalize ${filter === f ? 'bg-dgPrimary text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200'}`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>
      
      <div className="bg-white dark:bg-gray-800 rounded shadow overflow-hidden border dark:border-gray-700">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-100 dark:bg-gray-700 border-b dark:border-gray-600">
              <th className="p-4">Type</th>
              <th className="p-4">Reason</th>
              <th className="p-4">Status</th>
              <th className="p-4">Date</th>
              <th className="p-4">Assigned To</th>
              <th className="p-4">Action</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={6} className="p-4 text-center">Loading...</td></tr>
            ) : items.length === 0 ? (
              <tr><td colSpan={6} className="p-4 text-center text-gray-500">No items found.</td></tr>
            ) : items.map(item => (
              <tr key={item.id} className="border-b dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-750">
                <td className="p-4 font-medium">{item.itemType}</td>
                <td className="p-4 text-gray-600 dark:text-gray-300">{item.reason}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs font-semibold uppercase tracking-wider ${statusColors[item.status]}`}>
                    {item.status}
                  </span>
                </td>
                <td className="p-4 text-sm text-gray-500 dark:text-gray-400">{item.createdDate}</td>
                <td className="p-4 text-sm">{item.assignedTo}</td>
                <td className="p-4">
                  <Link href={`/review/${item.id}`} className="text-dgPrimary hover:underline font-medium">Review</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
