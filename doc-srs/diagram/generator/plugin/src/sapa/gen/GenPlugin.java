package sapa.gen;

import com.vp.plugin.*;
import com.vp.plugin.diagram.*;
import com.vp.plugin.model.*;
import com.vp.plugin.model.factory.IModelElementFactory;

import java.awt.Point;
import java.io.*;
import java.util.*;

/**
 * Headless Visual Paradigm plugin: reads a tab-separated diagram spec and builds
 * the diagrams with VP's Open API, then saves the project.
 * Invoke: Plugin -project X.vpp -pluginid sapa.gen -pluginargs "'spec.tsv' 'out.vpp'"
 */
public class GenPlugin implements VPPlugin, VPPluginCommandLineSupport {
    private final Map<String, IModelElement> models = new HashMap<>();
    private final Map<String, IShapeUIModel> shapes = new HashMap<>();
    private DiagramManager dm;
    private IModelElementFactory f;
    private IDiagramUIModel diagram;
    private int line;

    public void loaded(VPPluginInfo info) {}
    public void unloaded() {}

    public void invoke(String[] args) {
        try {
            dm = ApplicationManager.instance().getDiagramManager();
            f = IModelElementFactory.instance();
            try (BufferedReader r = new BufferedReader(new InputStreamReader(new FileInputStream(args[0]), "UTF-8"))) {
                String s;
                while ((s = r.readLine()) != null) {
                    line++;
                    if (s.trim().isEmpty() || s.startsWith("#")) continue;
                    try {
                        exec(s.split("\t", -1));
                    } catch (Throwable t) {
                        System.out.println("[sapa.gen] line " + line + " failed: " + s);
                        t.printStackTrace(System.out);
                    }
                }
            }
            boolean ok = ApplicationManager.instance().getProjectManager().saveProjectAs(new File(args[1]));
            System.out.println("[sapa.gen] saved=" + ok + " -> " + args[1]);
        } catch (Throwable t) {
            t.printStackTrace(System.out);
        }
    }

    private void exec(String[] p) {
        switch (p[0]) {
            case "DIAGRAM": diagram(p[1], p[2]); break;
            case "SHAPE": shape(p); break;
            case "PARENT": parent(p[1], p[2]); break;
            case "ATTR": attr(p[1], p[2]); break;
            case "OP": op(p[1], p[2], p.length > 3 ? p[3] : "", p.length > 4 ? p[4] : ""); break;
            case "CONN": conn(p); break;
            case "ACT": act(p[1], p[2], Integer.parseInt(p[3]), Integer.parseInt(p[4])); break;
            default: System.out.println("[sapa.gen] unknown command " + p[0]);
        }
    }

    private void diagram(String type, String name) {
        String t;
        switch (type) {
            case "usecase": t = DiagramManager.DIAGRAM_TYPE_USE_CASE_DIAGRAM; break;
            case "class": t = DiagramManager.DIAGRAM_TYPE_CLASS_DIAGRAM; break;
            case "sequence": t = DiagramManager.DIAGRAM_TYPE_INTERACTION_DIAGRAM; break;
            case "activity": t = DiagramManager.DIAGRAM_TYPE_ACTIVITY_DIAGRAM; break;
            default: throw new IllegalArgumentException(type);
        }
        diagram = dm.createDiagram(t);
        diagram.setName(name);
        models.clear();
        shapes.clear();
        acts.clear();
    }

    // SHAPE id kind x y w h name [extra]
    private void shape(String[] p) {
        String id = p[1], kind = p[2], name = p[7].replace("\\n", "\n"), extra = p.length > 8 ? p[8] : "";
        int x = Integer.parseInt(p[3]), y = Integer.parseInt(p[4]), w = Integer.parseInt(p[5]), h = Integer.parseInt(p[6]);
        IModelElement m;
        switch (kind) {
            case "actor": m = f.createActor(); break;
            case "usecase": m = f.createUseCase(); break;
            case "system": m = f.createSystem(); break;
            case "class": m = f.createClass(); break;
            case "lifeline": {
                IInteractionLifeLine l = f.createInteractionLifeLine();
                if (!extra.isEmpty()) l.addStereotype(extra);
                m = l;
                break;
            }
            case "iactor": m = f.createInteractionActor(); break;
            case "frame": m = f.createFrame(); break;
            case "action": m = f.createActivityAction(); break;
            case "decision": m = f.createDecisionNode(); break;
            case "merge": m = f.createMergeNode(); break;
            case "initial": m = f.createInitialNode(); break;
            case "final": m = f.createActivityFinalNode(); break;
            case "partition": m = f.createActivityPartition(); break;
            case "swimlane": {
                IActivitySwimlane2 sl = f.createActivitySwimlane2();
                for (String pn : extra.split("\\|")) {
                    IActivityPartition part = f.createActivityPartition();
                    part.setName(pn);
                    sl.addVerticalPartition(part);
                }
                m = sl;
                break;
            }
            default: throw new IllegalArgumentException(kind);
        }
        m.setName(name);
        IShapeUIModel s = (IShapeUIModel) dm.createDiagramElement(diagram, m);
        s.setBounds(x, y, w, h);
        if (kind.equals("system") || extra.equals("white")) s.getFillColor().setColor1(java.awt.Color.WHITE, true);
        resetCaption(s);
        models.put(id, m);
        shapes.put(id, s);
    }

    private final Map<String, List<Object[]>> acts = new HashMap<>();

    // ACT id lifeline y1 y2 : activation bar on a lifeline
    private void act(String id, String lifeline, int y1, int y2) {
        IInteractionLifeLine l = (IInteractionLifeLine) models.get(lifeline);
        IShapeUIModel ls = shapes.get(lifeline);
        IActivation a = f.createActivation();
        l.addActivation(a);
        IShapeUIModel as = (IShapeUIModel) dm.createDiagramElement(diagram, a);
        ls.addChild(as);
        as.setBounds(ls.getX() + ls.getWidth() / 2 - 6, y1, 12, y2 - y1);
        models.put(id, a);
        shapes.put(id, as);
        acts.computeIfAbsent(lifeline, k -> new ArrayList<>()).add(new Object[]{a, y1, y2, as});
    }

    private Object[] activationAt(String lifeline, int y) {
        for (Object[] a : acts.getOrDefault(lifeline, Collections.emptyList()))
            if ((int) a[1] <= y && y <= (int) a[2]) return a;
        return null;
    }

    private void parent(String child, String parent) {
        IModelElement pm = models.get(parent), cm = models.get(child);
        if (pm instanceof IHasChildrenBaseModelElement) ((IHasChildrenBaseModelElement) pm).addChild(cm);
        shapes.get(parent).addChild(shapes.get(child));
    }

    private void attr(String cls, String name) {
        IClass c = (IClass) models.get(cls);
        IAttribute a = f.createAttribute();
        a.setName(name);
        a.setVisibility("private");
        c.addAttribute(a);
    }

    private void op(String cls, String name, String param, String ret) {
        IClass c = (IClass) models.get(cls);
        IOperation o = f.createOperation();
        o.setName(name);
        o.setVisibility("public");
        if (!param.isEmpty()) {
            IParameter pa = f.createParameter();
            pa.setName(param);
            o.addParameter(pa);
        }
        if (!ret.isEmpty()) o.setReturnType(ret);
        c.addOperation(o);
    }

    private static Point[] parsePoints(String v) {
        if (v == null || v.isEmpty()) return null;
        String[] parts = v.split(";");
        Point[] r = new Point[parts.length];
        for (int i = 0; i < parts.length; i++) {
            String[] xy = parts[i].split(",");
            r[i] = new Point(Integer.parseInt(xy[0]), Integer.parseInt(xy[1]));
        }
        return r;
    }

    // CONN kind from to label [seq] [y] [points x,y;x,y] [caption x,y]
    private void conn(String[] p) {
        String kind = p[1], from = p[2], to = p[3], label = p.length > 4 ? p[4] : "";
        IShapeUIModel fs = shapes.get(from), ts = shapes.get(to);
        IModelElement fm = models.get(from), tm = models.get(to);
        Point[] pts = null;
        IModelElement rel;
        String shown = label;
        switch (kind) {
            case "assoc": {
                IAssociation a = f.createAssociation();
                a.setFrom(fm); a.setTo(tm);
                rel = a;
                break;
            }
            case "include": {
                IInclude i = f.createInclude();
                i.setFrom(fm); i.setTo(tm);
                shown = "<<Include>>";
                rel = i;
                break;
            }
            case "flow": {
                IControlFlow c = f.createControlFlow();
                c.setFrom(fm); c.setTo(tm);
                if (!label.isEmpty()) c.setGuard(label);
                shown = label.isEmpty() ? "" : "[" + label + "]";
                pts = parsePoints(p.length > 7 ? p[7] : "");
                rel = c;
                label = "";
                break;
            }
            case "msg": case "ret": case "self": {
                IMessage m = f.createMessage();
                m.setFrom(fm); m.setTo(tm);
                String seq = p.length > 5 ? p[5] : "";
                if (!seq.isEmpty()) m.setSequenceNumber(seq);
                shown = (seq.isEmpty() ? "" : seq + ": ") + label;
                int y = Integer.parseInt(p[6]);
                if (kind.equals("ret")) m.setActionType(f.createActionTypeReturn());
                if (kind.equals("self")) m.setType(IMessage.TYPE_SELF_MESSAGE);
                int fx = fs.getX() + fs.getWidth() / 2, tx = ts.getX() + ts.getWidth() / 2;
                Object[] fa = activationAt(from, y), ta = activationAt(to, kind.equals("self") ? y + 20 : y);
                if (fa != null) { m.setFromActivation((IActivation) fa[0]); fs = (IShapeUIModel) fa[3]; }
                if (ta != null) { m.setToActivation((IActivation) ta[0]); ts = (IShapeUIModel) ta[3]; }
                if (kind.equals("self")) {
                    pts = new Point[]{new Point(fx + 6, y), new Point(fx + 40, y), new Point(fx + 40, y + 20), new Point(fx + 6, y + 20)};
                } else {
                    int fxe = fa != null ? (tx > fx ? fx + 6 : fx - 6) : fx;
                    int txe = ta != null ? (tx > fx ? tx - 6 : tx + 6) : tx;
                    pts = new Point[]{new Point(fxe, y), new Point(txe, y)};
                }
                rel = m;
                break;
            }
            default: throw new IllegalArgumentException(kind);
        }
        if (!label.isEmpty()) rel.setName(label);
        IDiagramElement c = dm.createConnector(diagram, rel, fs, ts, pts);
        resetCaption(c);
        if (c != null && !shown.isEmpty()) {
            placeCaption(c, kind, shown, fs, ts, pts);
            Point[] cp = parsePoints(p.length > 8 ? p[8] : "");
            if (cp != null && c.getCaptionUIModel() != null) {
                ICaptionUIModel cap = c.getCaptionUIModel();
                cap.setBounds(cp[0].x, cp[0].y, cap.getWidth(), cap.getHeight());
            }
        }
    }

    /** Headless export does not lay out connector captions, so place them explicitly. */
    private static void placeCaption(IDiagramElement c, String kind, String text, IShapeUIModel fs, IShapeUIModel ts, Point[] pts) {
        ICaptionUIModel cap = c.getCaptionUIModel();
        if (cap == null) return;
        int w = (int) Math.round(text.length() * 6.4) + 14, h = 16;
        int x, y;
        if (pts != null && kind.equals("self")) {
            x = pts[0].x + 44; y = pts[0].y + 2;
        } else if (pts != null) {
            x = (pts[0].x + pts[1].x) / 2 - w / 2; y = pts[0].y - h - 2;
        } else {
            int fx = fs.getX() + fs.getWidth() / 2, fy = fs.getY() + fs.getHeight() / 2;
            int tx = ts.getX() + ts.getWidth() / 2, ty = ts.getY() + ts.getHeight() / 2;
            x = (fx + tx) / 2 + 6; y = (fy + ty) / 2 - h / 2;
            if (kind.equals("include")) { x = (fx + tx) / 2 - w / 2; y = (fy + ty) / 2 - h - 2; }
        }
        cap.setSide(ICaptionUIModel.SIDE_FREEMOVE);
        cap.setBounds(x, y, w, h);
        cap.setVisible(true);
    }

    private static void resetCaption(IDiagramElement e) {
        if (e == null) return;
        e.setRequestResetCaption(true);
        e.setRequestResetCaptionSize(true);
        e.setRequestResetCaptionFitWidth(true);
    }
}
