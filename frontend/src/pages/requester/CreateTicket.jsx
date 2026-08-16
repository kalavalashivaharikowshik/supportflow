import {
  useState,
} from "react";

import {
  useNavigate,
} from "react-router";

import toast from "react-hot-toast";

import Button from "../../components/common/Button";
import Input from "../../components/common/Input";
import PageHeader from "../../components/common/PageHeader";
import Select from "../../components/common/Select";
import Textarea from "../../components/common/Textarea";

import {
  PRIORITY_OPTIONS,
} from "../../constants/priorities";

import {
  getTicketDetailsRoute,
} from "../../constants/routes";

import {
  createTicket,
} from "../../services/ticketService";

import {
  getApiErrorMessage,
} from "../../utils/apiError";

import {
  required,
} from "../../utils/validation";


const CATEGORY_OPTIONS = [
  {
    value: "GENERAL",
    label: "General",
  },
  {
    value: "TECHNICAL",
    label: "Technical",
  },
  {
    value: "ACCESS",
    label: "Access",
  },
  {
    value: "BILLING",
    label: "Billing",
  },
];


function CreateTicket() {
  const navigate =
    useNavigate();

  const [form, setForm] =
    useState({
      title: "",
      description: "",
      category: "",
      priority: "",
    });

  const [errors, setErrors] =
    useState({});

  const [loading, setLoading] =
    useState(false);


  const handleChange = (
    event
  ) => {
    const {
      name,
      value,
    } = event.target;

    setForm(
      (current) => ({
        ...current,
        [name]: value,
      })
    );

    setErrors(
      (current) => ({
        ...current,
        [name]: "",
      })
    );
  };


  const validate = () => {
    const nextErrors = {
      title: required(
        form.title,
        "Title"
      ),

      description: required(
        form.description,
        "Description"
      ),

      category: required(
        form.category,
        "Category"
      ),

      priority: required(
        form.priority,
        "Priority"
      ),
    };


    if (
      form.title.trim() &&
      form.title.trim()
        .length < 5
    ) {
      nextErrors.title =
        "Title must contain at least 5 characters.";
    }


    if (
      form.description.trim() &&
      form.description.trim()
        .length < 10
    ) {
      nextErrors.description =
        "Description must contain at least 10 characters.";
    }


    Object.keys(
      nextErrors
    ).forEach(
      (key) => {
        if (!nextErrors[key]) {
          delete nextErrors[key];
        }
      }
    );

    setErrors(nextErrors);

    return (
      Object.keys(nextErrors)
        .length === 0
    );
  };


  const handleSubmit =
    async (event) => {
      event.preventDefault();

      if (!validate()) {
        return;
      }

      setLoading(true);

      try {
        const ticket =
          await createTicket({
            title:
              form.title.trim(),

            description:
              form.description.trim(),

            category:
              form.category,

            priority:
              form.priority,
          });

        toast.success(
          "Ticket created successfully."
        );

        navigate(
          getTicketDetailsRoute(
            ticket.id
          )
        );
      } catch (error) {
        toast.error(
          getApiErrorMessage(
            error,
            "Unable to create ticket."
          )
        );
      } finally {
        setLoading(false);
      }
    };


  return (
    <div className="space-y-6">
      <PageHeader
        title="Create Ticket"
        description="Submit a new support request and select its priority."
      />

      <form
        onSubmit={handleSubmit}
        className="
          max-w-3xl space-y-5
          rounded-xl border
          border-slate-200
          bg-white p-6
          shadow-sm
        "
      >
        <Input
          id="title"
          name="title"
          label="Title"
          placeholder="Briefly describe the issue"
          value={form.title}
          onChange={handleChange}
          error={errors.title}
        />

        <Textarea
          id="description"
          name="description"
          label="Description"
          placeholder="Explain the issue, impact, and any useful details."
          value={
            form.description
          }
          onChange={handleChange}
          error={
            errors.description
          }
        />

        <div
          className="
            grid gap-4
            sm:grid-cols-2
          "
        >
          <Select
            id="category"
            name="category"
            label="Category"
            options={
              CATEGORY_OPTIONS
            }
            value={
              form.category
            }
            onChange={handleChange}
            error={
              errors.category
            }
          />

          <Select
            id="priority"
            name="priority"
            label="Priority"
            options={
              PRIORITY_OPTIONS
            }
            value={
              form.priority
            }
            onChange={handleChange}
            error={
              errors.priority
            }
          />
        </div>

        <div
          className="
            flex justify-end
          "
        >
          <Button
            type="submit"
            loading={loading}
          >
            Create ticket
          </Button>
        </div>
      </form>
    </div>
  );
}


export default CreateTicket;