import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  User,
  UserPlus,
  Calendar,
  ClipboardList,
  CheckCircle2,
  AlertCircle,
  Loader2,
} from "lucide-react";

/**
 * Esquema de validación con Zod
 */
const attendanceSchema = z.object({
  fecha: z.string().min(1, { message: "La fecha es requerida" }),
  atletaNombre: z
    .string()
    .min(3, {
      message: "El nombre del atleta debe tener al menos 3 caracteres",
    }),
  entrenadorNombre: z
    .string()
    .min(3, {
      message: "El nombre del entrenador debe tener al menos 3 caracteres",
    }),
  auxiliarNombre: z
    .string()
    .min(3, {
      message: "El nombre del auxiliar debe tener al menos 3 caracteres",
    }),
  observaciones: z.string().optional(),
});

type AttendanceFormData = z.infer<typeof attendanceSchema>;

export default function AttendanceForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<
    "idle" | "success" | "error"
  >("idle");

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AttendanceFormData>({
    resolver: zodResolver(attendanceSchema),
    defaultValues: {
      fecha: new Date().toISOString().split("T")[0], // Fecha de hoy por defecto
      observaciones: "",
    },
  });

  const onSubmit = async (data: AttendanceFormData) => {
    setIsSubmitting(true);
    setSubmitStatus("idle");

    // Simulación de envío a una API o Base de Datos
    try {
      console.log("Datos del formulario:", data);
      await new Promise((resolve) => setTimeout(resolve, 1500)); // Simular retraso
      setSubmitStatus("success");
      reset(); // Limpiar el formulario tras éxito

      // Volver al estado inicial después de 3 segundos
      setTimeout(() => setSubmitStatus("idle"), 4000);
    } catch (error) {
      setSubmitStatus("error");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4 font-sans">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-xl overflow-hidden border border-slate-100">
        {/* Encabezado */}
        <div className="bg-blue-600 p-8 text-white">
          <div className="flex items-center gap-3 mb-2">
            <ClipboardList className="w-8 h-8" />
            <h1 className="text-2xl font-bold tracking-tight">
              Registro de Asistencia
            </h1>
          </div>
          <p className="text-blue-100 opacity-90">
            Complete los campos para registrar la actividad del atleta.
          </p>
        </div>

        {/* Formulario */}
        <form onSubmit={handleSubmit(onSubmit)} className="p-8 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Campo: Fecha */}
            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                <Calendar className="w-4 h-4 text-blue-500" />
                Fecha
              </label>
              <input
                type="date"
                {...register("fecha")}
                className={`p-3 bg-slate-50 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all ${
                  errors.fecha ? "border-red-500" : "border-slate-200"
                }`}
              />
              {errors.fecha && (
                <span className="text-xs text-red-500 mt-1 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" /> {errors.fecha.message}
                </span>
              )}
            </div>

            {/* Campo: Nombre del Atleta */}
            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                <User className="w-4 h-4 text-blue-500" />
                Nombre y Apellido del Atleta
              </label>
              <input
                placeholder="Ej: Juan Pérez"
                {...register("atletaNombre")}
                className={`p-3 bg-slate-50 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all ${
                  errors.atletaNombre ? "border-red-500" : "border-slate-200"
                }`}
              />
              {errors.atletaNombre && (
                <span className="text-xs text-red-500 mt-1 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />{" "}
                  {errors.atletaNombre.message}
                </span>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Campo: Entrenador */}
            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                <UserPlus className="w-4 h-4 text-blue-500" />
                Entrenador a Cargo
              </label>
              <input
                placeholder="Nombre del entrenador"
                {...register("entrenadorNombre")}
                className={`p-3 bg-slate-50 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all ${
                  errors.entrenadorNombre
                    ? "border-red-500"
                    : "border-slate-200"
                }`}
              />
              {errors.entrenadorNombre && (
                <span className="text-xs text-red-500 mt-1 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />{" "}
                  {errors.entrenadorNombre.message}
                </span>
              )}
            </div>

            {/* Campo: Auxiliar */}
            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
                <UserPlus className="w-4 h-4 text-blue-500" />
                Auxiliar a Cargo
              </label>
              <input
                placeholder="Nombre del auxiliar"
                {...register("auxiliarNombre")}
                className={`p-3 bg-slate-50 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all ${
                  errors.auxiliarNombre ? "border-red-500" : "border-slate-200"
                }`}
              />
              {errors.auxiliarNombre && (
                <span className="text-xs text-red-500 mt-1 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />{" "}
                  {errors.auxiliarNombre.message}
                </span>
              )}
            </div>
          </div>

          {/* Campo: Observaciones */}
          <div className="flex flex-col gap-2">
            <label className="text-sm font-semibold text-slate-700 flex items-center gap-2">
              <ClipboardList className="w-4 h-4 text-blue-500" />
              Observaciones
            </label>
            <textarea
              placeholder="Detalles adicionales sobre la sesión o el estado del atleta..."
              rows={4}
              {...register("observaciones")}
              className="p-3 bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all resize-none"
            />
          </div>

          {/* Feedback de Estado */}
          {submitStatus === "success" && (
            <div className="bg-green-50 text-green-700 p-4 rounded-lg flex items-center gap-3 border border-green-200 animate-in fade-in zoom-in duration-300">
              <CheckCircle2 className="w-5 h-5 text-green-600" />
              <p className="text-sm font-medium">
                ¡Asistencia registrada exitosamente!
              </p>
            </div>
          )}

          {submitStatus === "error" && (
            <div className="bg-red-50 text-red-700 p-4 rounded-lg flex items-center gap-3 border border-red-200">
              <AlertCircle className="w-5 h-5 text-red-600" />
              <p className="text-sm font-medium">
                Hubo un error al guardar los datos. Intente nuevamente.
              </p>
            </div>
          )}

          {/* Botón de Envío */}
          <button
            type="submit"
            disabled={isSubmitting}
            className={`w-full py-4 px-6 rounded-xl text-white font-bold text-lg shadow-lg shadow-blue-200 transition-all active:scale-95 flex items-center justify-center gap-2 ${
              isSubmitting
                ? "bg-blue-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Procesando...
              </>
            ) : (
              "Registrar Asistencia"
            )}
          </button>
        </form>

        <div className="p-4 bg-slate-50 border-t border-slate-100 text-center">
          <p className="text-xs text-slate-400 font-medium uppercase tracking-widest">
            Sistema de Gestión Deportiva
          </p>
        </div>
      </div>
    </div>
  );
}
