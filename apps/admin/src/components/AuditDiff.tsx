export default function AuditDiff({ before, after }: { before: any, after: any }) {
  return (
    <div className="grid grid-cols-2 gap-4 text-sm font-mono">
      <div className="p-4 bg-red-50 rounded border border-red-100">
        <h4 className="text-red-800 font-bold mb-2">Before</h4>
        <pre className="text-red-900 whitespace-pre-wrap">{JSON.stringify(before, null, 2)}</pre>
      </div>
      <div className="p-4 bg-green-50 rounded border border-green-100">
        <h4 className="text-green-800 font-bold mb-2">After</h4>
        <pre className="text-green-900 whitespace-pre-wrap">{JSON.stringify(after, null, 2)}</pre>
      </div>
    </div>
  );
}
