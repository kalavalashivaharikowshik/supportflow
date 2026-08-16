import apiClient from "../api/apiClient";


export const getTicketReportSummary =
  async (
    params = {}
  ) => {
    const response =
      await apiClient.get(
        "/reports/tickets/summary",
        {
          params,
        }
      );

    return response.data;
  };


export const getSlaBreachReport =
  async (
    params = {}
  ) => {
    const response =
      await apiClient.get(
        "/reports/sla-breaches",
        {
          params,
        }
      );

    return response.data;
  };


export const getAgentPerformanceReport =
  async (
    params = {}
  ) => {
    const response =
      await apiClient.get(
        "/reports/agents/performance",
        {
          params,
        }
      );

    return response.data;
  };


const downloadCsv = async (
  url,
  filename,
  params = {}
) => {
  const response =
    await apiClient.get(
      url,
      {
        params,
        responseType: "blob",
      }
    );

  const blobUrl =
    window.URL.createObjectURL(
      response.data
    );

  const link =
    document.createElement("a");

  link.href = blobUrl;
  link.download = filename;

  document.body.appendChild(
    link
  );

  link.click();

  link.remove();

  window.URL.revokeObjectURL(
    blobUrl
  );
};


export const downloadTicketReport =
  async (
    params = {}
  ) => {
    return downloadCsv(
      "/reports/tickets/export",
      "supportflow-tickets.csv",
      params
    );
  };


export const downloadSlaReport =
  async (
    params = {}
  ) => {
    return downloadCsv(
      "/reports/sla-breaches/export",
      "supportflow-sla-breaches.csv",
      params
    );
  };


export const downloadAgentReport =
  async (
    params = {}
  ) => {
    return downloadCsv(
      "/reports/agents/performance/export",
      "supportflow-agent-performance.csv",
      params
    );
  };