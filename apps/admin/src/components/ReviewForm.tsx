'use client';
import { useState } from 'react';

export default function ReviewForm({ itemId }: { itemId: string }) {
  const [decision, setDecision] = useState('');
  const [notes, setNotes] = useState('');

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Review Decision</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Decision</label>
          <select 
            value={decision}
            onChange={(e) => setDecision(e.target.value)}
            className="w-full p-2 border rounded"
          >
            <option value="">Select...</option>
            <option value="approve">Approve & Merge</option>
            <option value="reject">Reject</option>
            <option value="defer">Defer for Field Verification</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Notes</label>
          <textarea 
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            className="w-full p-2 border rounded h-24"
            placeholder="Add context to your decision..."
          />
        </div>
        <button className="bg-dgPrimary text-white px-4 py-2 rounded font-medium">
          Submit Decision
        </button>
      </div>
    </div>
  );
}
