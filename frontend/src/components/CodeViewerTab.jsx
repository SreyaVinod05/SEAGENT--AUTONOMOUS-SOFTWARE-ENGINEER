import React, { useState } from 'react'
import {
  FileCode,
  Download,
  Copy,
  Check,
  Folder,
  File,
  Terminal,
} from 'lucide-react'
import { downloadProjectZip } from '../services/api'

export default function CodeViewerTab({ workflowId, files }) {
  const [selectedPath, setSelectedPath] = useState(files?.[0]?.path || '')
  const [copied, setCopied] = useState(false)

  if (!files || files.length === 0) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
        Source code generation not yet reached.
      </div>
    )
  }

  const selectedFile = files.find((f) => f.path === selectedPath) || files[0]

  const handleCopy = () => {
    if (selectedFile?.content) {
      navigator.clipboard.writeText(selectedFile.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const handleDownload = () => {
    if (workflowId) {
      downloadProjectZip(workflowId)
    }
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: '20px', minHeight: '560px' }}>
      {/* File Explorer Tree */}
      <div className="glass-panel" style={{ padding: '18px', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', fontWeight: '700' }}>
            <Folder size={18} color="#818cf8" />
            <span>Files ({files.length})</span>
          </div>
          <button
            onClick={handleDownload}
            className="btn-secondary"
            title="Download ZIP archive"
            style={{ padding: '5px 8px', fontSize: '0.75rem' }}
          >
            <Download size={14} /> ZIP
          </button>
        </div>

        {/* File List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', overflowY: 'auto', flex: 1 }}>
          {files.map((file) => {
            const isSelected = file.path === selectedFile?.path
            const isTest = file.path.includes('test')
            const isMd = file.path.endsWith('.md')

            return (
              <button
                key={file.path}
                onClick={() => setSelectedPath(file.path)}
                style={{
                  background: isSelected ? 'rgba(99, 102, 241, 0.15)' : 'transparent',
                  border: isSelected ? '1px solid rgba(99, 102, 241, 0.4)' : '1px solid transparent',
                  borderRadius: 'var(--radius-sm)',
                  padding: '8px 10px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  color: isSelected ? '#ffffff' : 'var(--text-muted)',
                  fontSize: '0.82rem',
                  cursor: 'pointer',
                  textAlign: 'left',
                  transition: 'all 0.15s ease',
                  fontFamily: 'var(--font-mono)',
                }}
              >
                {isTest ? (
                  <Terminal size={15} color="#34d399" />
                ) : isMd ? (
                  <File size={15} color="#f59e0b" />
                ) : (
                  <FileCode size={15} color="#818cf8" />
                )}
                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {file.path}
                </span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Code Viewer Panel */}
      <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column' }}>
        {/* File Top Bar */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderBottom: '1px solid var(--border-subtle)',
          paddingBottom: '12px',
          marginBottom: '16px',
        }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FileCode size={18} color="#818cf8" />
              <span style={{ fontWeight: '700', fontSize: '0.95rem', fontFamily: 'var(--font-mono)' }}>
                {selectedFile?.path}
              </span>
            </div>
            {selectedFile?.description && (
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                {selectedFile.description}
              </div>
            )}
          </div>

          <div style={{ display: 'flex', gap: '8px' }}>
            <button className="btn-secondary" onClick={handleCopy} style={{ fontSize: '0.8rem', padding: '6px 12px' }}>
              {copied ? <Check size={14} color="#34d399" /> : <Copy size={14} />}
              <span>{copied ? 'Copied!' : 'Copy Code'}</span>
            </button>
            <button className="btn-primary" onClick={handleDownload} style={{ fontSize: '0.8rem', padding: '6px 14px' }}>
              <Download size={14} />
              <span>Download Project</span>
            </button>
          </div>
        </div>

        {/* Code Content */}
        <div className="code-container" style={{ flex: 1, padding: '16px', maxHeight: '580px' }}>
          <pre style={{ margin: 0 }}>
            <code>{selectedFile?.content}</code>
          </pre>
        </div>
      </div>
    </div>
  )
}
