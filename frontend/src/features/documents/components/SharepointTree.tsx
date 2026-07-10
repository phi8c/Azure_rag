import { useState } from "react";
import { ChevronDown, ChevronRight, Folder, FolderOpen, Building2, Library } from "lucide-react";

export interface SharePointFolder { id: string; name: string; children?: SharePointFolder[]; }
export interface SharePointDrive { id: string; name: string; folders: SharePointFolder[]; }
export interface SharePointSite { id: string; name: string; libraries: SharePointDrive[]; }
export interface SelectedLocation { siteId: string; siteName: string; driveId: string; driveName: string; folderId?: string; folderName?: string; }
export interface SharePointTreeProps { data: SharePointSite[]; selectedLocation: SelectedLocation | null; onSelectLocation: (location: SelectedLocation) => void; }

interface TreeNodeProps { site: SharePointSite; drive: SharePointDrive; folder: SharePointFolder; level: number; expanded: Record<string, boolean>; toggle: (id: string) => void; selectedLocation: SelectedLocation | null; onSelectLocation: (location: SelectedLocation) => void; }

const TreeNode = ({ site, drive, folder, level, expanded, toggle, selectedLocation, onSelectLocation }: TreeNodeProps) => {
    const hasChildren = (folder.children?.length ?? 0) > 0;
    const isExpanded = expanded[folder.id] ?? false;
    const isSelected = selectedLocation?.folderId === folder.id;

    return (
        <>
            <div onClick={() => { onSelectLocation({ siteId: site.id, siteName: site.name, driveId: drive.id, driveName: drive.name, folderId: folder.id, folderName: folder.name }); if (hasChildren) toggle(folder.id); }} style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", padding: "6px 10px", paddingLeft: 16 + level * 20, borderRadius: 6, background: isSelected ? "#DBEAFE" : "transparent", userSelect: "none" }}>
                {hasChildren ? (isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />) : <div style={{ width: 16 }} />}
                {isExpanded ? <FolderOpen size={18} color={isSelected ? "#2563EB" : "#D97706"} /> : <Folder size={18} color={isSelected ? "#2563EB" : "#D97706"} />}
                <span style={{ color: "#111827", fontWeight: isSelected ? 600 : 400 }}>{folder.name}</span>
            </div>

            {hasChildren && isExpanded && folder.children!.map((child) => <TreeNode key={child.id} site={site} drive={drive} folder={child} level={level + 1} expanded={expanded} toggle={toggle} selectedLocation={selectedLocation} onSelectLocation={onSelectLocation} />)}
        </>
    );
};

const SharePointTree = ({ data, selectedLocation, onSelectLocation }: SharePointTreeProps) => {
    const [expanded, setExpanded] = useState<Record<string, boolean>>({});
    const toggle = (id: string) => setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));

    return (
        <div style={{ border: "1px solid #E5E7EB", borderRadius: 8, padding: 12, height: 450, overflowY: "auto", background: "#FFF", color: "#111827" }}>
            {data.map((site) => {
                const siteExpanded = expanded[site.id] ?? true;
                return (
                    <div key={site.id}>
                        <div onClick={() => toggle(site.id)} style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", padding: "8px 6px", fontWeight: 600 }}>{siteExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}<Building2 size={18} /><span>{site.name}</span></div>

                        {siteExpanded && site.libraries.map((drive) => {
                            const driveExpanded = expanded[drive.id] ?? true;
                            const driveSelected = selectedLocation?.driveId === drive.id && !selectedLocation?.folderId;

                            return (
                                <div key={drive.id}>
                                    <div onClick={() => { onSelectLocation({ siteId: site.id, siteName: site.name, driveId: drive.id, driveName: drive.name }); toggle(drive.id); }} style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", padding: "6px 10px", paddingLeft: 28, borderRadius: 6, background: driveSelected ? "#DBEAFE" : "transparent" }}>
                                        {driveExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                                        <Library size={18} color={driveSelected ? "#2563EB" : "#6B7280"} />
                                        <span style={{ color: "#111827", fontWeight: driveSelected ? 600 : 400 }}>{drive.name}</span>
                                    </div>

                                    {driveExpanded && drive.folders.map((folder) => <TreeNode key={folder.id} site={site} drive={drive} folder={folder} level={2} expanded={expanded} toggle={toggle} selectedLocation={selectedLocation} onSelectLocation={onSelectLocation} />)}
                                </div>
                            );
                        })}
                    </div>
                );
            })}
        </div>
    );
};

export default SharePointTree;