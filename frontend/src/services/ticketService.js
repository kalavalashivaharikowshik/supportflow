import apiClient from "../api/apiClient";


export const createTicket = async (
  payload
) => {
  const response = await apiClient.post(
    "/tickets",
    payload
  );

  return response.data;
};


export const getMyTickets = async (
  params = {}
) => {
  const response = await apiClient.get(
    "/tickets/my",
    {
      params,
    }
  );

  return response.data;
};


export const getTicketById = async (
  ticketId
) => {
  const response = await apiClient.get(
    `/tickets/${ticketId}`
  );

  return response.data;
};


export const getTicketResponses = async (
  ticketId
) => {
  const response = await apiClient.get(
    `/tickets/${ticketId}/responses`
  );

  return response.data;
};


export const addTicketResponse = async (
  ticketId,
  payload
) => {
  const response = await apiClient.post(
    `/tickets/${ticketId}/responses`,
    payload
  );

  return response.data;
};


export const getTicketAudit = async (
  ticketId
) => {
  const response = await apiClient.get(
    `/tickets/${ticketId}/audit`
  );

  return response.data;
};


export const closeTicket = async (
  ticketId
) => {
  const response = await apiClient.patch(
    `/tickets/${ticketId}/close`
  );

  return response.data;
};


export const reopenTicket = async (
  ticketId
) => {
  const response = await apiClient.patch(
    `/tickets/${ticketId}/reopen`
  );

  return response.data;
};

export const getAssignedTickets = async (
  params = {}
) => {
  const response = await apiClient.get(
    "/tickets/assigned/me",
    {
      params,
    }
  );

  return response.data;
};


export const startTicketWork = async (
  ticketId
) => {
  const response = await apiClient.patch(
    `/tickets/assigned/${ticketId}/start`
  );

  return response.data;
};


export const resolveTicket = async (
  ticketId,
  payload
) => {
  const response = await apiClient.patch(
    `/tickets/assigned/${ticketId}/resolve`,
    payload
  );

  return response.data;
};

export const getAllTickets = async (
  params = {}
) => {
  const response = await apiClient.get(
    "/tickets/admin/all",
    {
      params,
    }
  );

  return response.data;
};


export const getAdminEscalatedTickets =
  async (
    params = {}
  ) => {
    const response =
      await apiClient.get(
        "/tickets/admin/escalated",
        {
          params,
        }
      );

    return response.data;
  };


export const assignTicket = async (
  ticketId,
  agentId
) => {
  const response =
    await apiClient.patch(
      `/tickets/admin/${ticketId}/assign`,
      {
        agent_id: agentId,
      }
    );

  return response.data;
};


export const reassignTicket = async (
  ticketId,
  agentId
) => {
  const response =
    await apiClient.patch(
      `/tickets/admin/${ticketId}/reassign`,
      {
        agent_id: agentId,
      }
    );

  return response.data;
};


export const updateTicketPriority =
  async (
    ticketId,
    priority
  ) => {
    const response =
      await apiClient.patch(
        `/tickets/admin/${ticketId}/priority`,
        {
          priority,
        }
      );

    return response.data;
  };