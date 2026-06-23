import {api} from "@/shared/api/axios";

export async function getGraph() {

  const { data } = await api.get(
    "/graph/visualize"
  );

  return data;
}

export async function askGraph(

  conversationId: string,

  question: string,

  role: string,

  email: string

) {

  const res =
    await api.post(

      "/think/graph",

      {

        conversation_id:
          conversationId,

        question,

        role,

        email

      }
    );

  return {

    answer:
      res.data?.answer
      ?? "",

    evidence:
      res.data?.evidence
      ?? []

  };
}

export async function activateSEF() {

  const { data } = await api.post(
    "/graph/completion"
  );

  return data;
}