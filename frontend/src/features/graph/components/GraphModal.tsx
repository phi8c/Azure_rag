import ForceGraph3D from
"react-force-graph-3d";

import { useGraph }
from "../hooks/useGraph";

type Props = {

  open: boolean;

  onClose: () => void;
};

export default function GraphModal({

  open,

  onClose

}: Props) {

  const {
    data,
    isLoading
  } = useGraph();

  if (!open) {
    return null;
  }

  return (

    <div
      style={{
        position: "fixed",
        inset: 0,
        background:
          "rgba(0,0,0,0.7)",
        zIndex: 9999
      }}
    >

      <div
        style={{
          width: "100vw",
          height: "100vh",
          background:
            "#000"
        }}
      >

        <button
          onClick={onClose}
          style={{
            position: "absolute",
            top: 20,
            right: 20,
            zIndex: 99999
          }}
        >
          Close
        </button>

        {isLoading ? (

          <div
            style={{
              color: "white",
              padding: 24
            }}
          >
            Loading...
          </div>

        ) : (

          <ForceGraph3D

            graphData={
              data
            }

            nodeLabel="name"

            linkLabel="label"

            nodeAutoColorBy=
            "type"

            nodeVal={(node: any) => {

  return (
    node.degree || 3
  );
}}

          />
        )}

      </div>

    </div>
  );
}